#!/usr/bin/python

import time
import datetime
import MySQLdb
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from datetime import datetime

sensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BOARD)

pinLight1 = 13
pinLight2 = 29
pinTemp1  = 4
pinTemp2  = 16
pinMotion = 16

pinLED1 = 37
pinLED2 = 35
pinLED3 = 33
pinLED4 = 31

MEAN_READING = 5

SEARCH_FOR_STEP = 0
READING_STEPS = 1
FINISHED = 2

class Measurement:
  def __init__(self):
    self.temp1  = -1
    self.temp2  = -1
    self.motion = True
    self.light1 = -1
    self.light2 = -1

  def readTemp(self):
  	try:
		i = 0
		while i<MEAN_READING:
			humidity1, temperature1 = Adafruit_DHT.read_retry(sensor,pinTemp1)
			humidity2, temperature2 = Adafruit_DHT.read_retry(sensor,pinTemp2)

			self.temp1 += temperature1
			self.temp2 += temperature2
			i += 1

			print 'Temp Inside {0:d}: {1:0.1f} C Humidity1: {2:0.1f} %'.format(i,temperature1,humidity1)
			print 'Temp Outside {0:d}: {1:0.1f} C Humidity2: {2:0.1f} %'.format(i,temperature2,humidity2)
	except KeyboardInterrupt:
		pass

	self.temp1 = self.temp1/MEAN_READING
	self.temp2 = self.temp2/MEAN_READING

  def readMotion(self):
	i = 0
	GPIO.setup(pinMotion,GPIO.IN)
	try:
		while i<MEAN_READING:
			if (GPIO.input(pinMotion)==True):
				print "Motion detected."
				self.motion = True
			else:
				print "Room empty!"
				self.motion = False
			time.sleep(1)
			i += 1
	except KeyboardInterrupt:
		pass

  def readLight(self):

	try:
		i = 0
		while i<MEAN_READING:
			count0 = 0
			count1 = 0

			GPIO.setup(pinLight1,GPIO.OUT)
			GPIO.output(pinLight1,GPIO.LOW)

			time.sleep(0.1)

			GPIO.setup(pinLight1,GPIO.IN)

			while (GPIO.input(pinLight1)==GPIO.LOW):
				count0 += 1

			GPIO.setup(pinLight2,GPIO.OUT)
			GPIO.output(pinLight2,GPIO.LOW)

			time.sleep(0.1)

			GPIO.setup(pinLight2,GPIO.IN)

			while (GPIO.input(pinLight2)==GPIO.LOW):
				count1 += 1

			self.light1 += count0
			self.light2 += count1
			i += 1

			print('Light Sensor Inside {0:d}: {1:d}'.format(i,self.light1))
			print('Light Sensor Outside {0:d}: {1:d}'.format(i,self.light2))
	except KeyboardInterrupt:
		pass

	self.light1 = self.light1/MEAN_READING
	self.light2 = self.light2/MEAN_READING

  def returnMeas(self):
    return self.temp1,self.temp2, self.light1, self.light2, self.motion

class FileHandler:
  def __init__(self,temp1,temp2,light1,light2,motion):
    self.temp1  = temp1
    self.temp2  = temp2
    self.motion = motion
    self.light1 = light1
    self.light2 = light2

  def storeMeasurements(self):
    file = open(r"/home/smartcities/Documents/Meas.txt","w")
    file.write(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + "\n")
    file.write("Temperature1 = %s \n" % self.temp1 )
    file.write("Temperature2 = %s \n" % self.temp2 )
    file.write("Light1 = %s \n" % self.light1 )
    file.write("Light2 = %s \n" % self.light2 )
    file.write("Motion = %s \n" % self.motion )
    file.close()

class DBHandler:
  def __init__(self,temp1,temp2,light1,light2,motion):
    self.temp1  = temp1
    self.temp2  = temp2
    self.motion = motion
    self.light1 = light1
    self.light2 = light2
    self.db     = None
    self.cursor = None

  def openDB(self):
    self.db     = MySQLdb.connect("localhost", "root", "smartcities", "smartcities")
    self.cursor = self.db.cursor()

  def insertNewMeas(self):
    sql = "INSERT INTO meas(date, \
       temp1, temp2, light1, light2, motion) \
       VALUES ('%s', '%f', '%f', '%d', '%d', '%d' )" % \
       (datetime.now().strftime("%Y-%m-%d | %H:%M:%S"), self.temp1, self.temp2, self.light1, self.light2, self.motion)

    try:
        # Execute the SQL command
        self.cursor.execute(sql)
        # Commit your changes in the database
        self.db.commit()
        print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Added in Database") 
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        # Rollback in case there is any error
	print(e)
        print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Error writing Database") 
        self.db.rollback()

  def insertNewOutput(self,radiator,window,blinds,lights):
	sql = "INSERT INTO output(radiator,blinds,window,lights) VALUES ('%s','%s','%s','%s')" % (radiator,blinds,window,lights)

	try:
		self.cursor.execute(sql)
		self.db.commit()
		print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Added in output Table")
	except (MySQLdb.Error,MySQLdb.Warning) as e:
		print(e)
		print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Error writing output Table")
		self.db.rollback()

  def closeDB(self):
    self.db.close()
    self.db     = None
    self.cursor = None

class PublisherHandler:
	def __init__(self):
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect

	def on_connect(self):
		print("Connected with result code "+str(rc))

	def myConnect(self):
		self.client.connect("localhost",1883,60)
		self.client.loop_start()

	def sendMessage(self,topic,msg):
		info = self.client.publish(topic,msg)
		info.wait_for_publish()

class StepsHandler:
	def __init__(self):
		self.auxSteps = []
		self.steps = []
		self.radiator = ""
		self.window = ""
		self.blinds = ""
		self.lights = ""

	def readOutputFile(self):
		ret = False
		with open("/home/smartcities/Documents/Output.txt") as fp:
			line = fp.readline()
			state = SEARCH_FOR_STEP
			while line:
				if (state==SEARCH_FOR_STEP):
					if "step" in line:
						print("STEP found")
						ret = True
						self.auxSteps.append(line.strip())
						state = READING_STEPS
				elif (state==READING_STEPS):
					if not line.strip():
						state = FINISHED
					else:
						self.auxSteps.append(line.strip())
				else:
					print("Finished to find steps")
					break
				line = fp.readline()
		fp.close()
		return ret

	def findSteps(self):
		i = 0
		while (i<len(self.auxSteps)):
			aux = self.auxSteps[i].split(":")
			aux1 = aux[1].split(" ")
			self.steps.append(aux1[1])
			i += 1

	def dumpSteps(self):
		i = 0
		while(i<len(self.steps)):
			print(self.steps[i])
			if ("RADIATOR" in self.steps[i]):
				self.radiator = self.steps[i]
			if ("WINDOW" in self.steps[i]):
				self.window = self.steps[i]
			if ("LIGHTS" in self.steps[i]):
				self.lights = self.steps[i]
			if ("BLINDS" in self.steps[i]):
				self.blinds = self.steps[i]
			i += 1

	def getRadiator(self):
		return self.radiator

	def getWindow(self):
		return self.window

	def getBlinds(self):
		return self.blinds

	def getLights(self):
		return self.lights


class LEDHandler:
	def __init__(self):
		GPIO.setup(pinLED1,GPIO.OUT)
		GPIO.setup(pinLED2,GPIO.OUT)
		GPIO.setup(pinLED3,GPIO.OUT)
		GPIO.setup(pinLED4,GPIO.OUT)

	def radiatorLED(self,value):
		if (value):
			GPIO.output(pinLED1,GPIO.HIGH)
		else:
			GPIO.output(pinLED1,GPIO.LOW)

	def windowLED(self,value):
		if (value):
			GPIO.output(pinLED2,GPIO.HIGH)
		else:
			GPIO.output(pinLED2,GPIO.LOW)

	def blindsLED(self,value):
		if (value):
			GPIO.output(pinLED3,GPIO.HIGH)
		else:
			GPIO.output(pinLED3,GPIO.LOW)

	def lightsLED(self,value):
		if (value):
			GPIO.output(pinLED4,GPIO.HIGH)
		else:
			GPIO.output(pinLED4,GPIO.LOW)

print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Measurement Script started") 
meas = Measurement()
meas.readTemp()
meas.readMotion()
meas.readLight()
print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Measurement Received") 
print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> DumpSensor: "+str(meas.returnMeas())) 

fileHandler = FileHandler(meas.returnMeas()[0],meas.returnMeas()[1],meas.returnMeas()[2],meas.returnMeas()[3],meas.returnMeas()[4])
fileHandler.storeMeasurements()
print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Stored in Meas.txt File") 

publisherHandler = PublisherHandler()
publisherHandler.myConnect()
publisherHandler.sendMessage("request/decision",str(meas.returnMeas()[0])+";"+str(meas.returnMeas()[1])+";"+str(meas.returnMeas()[2])+";"+str(meas.returnMeas()[3])+";"+str(int(meas.returnMeas()[4])))
time.sleep(5)
publisherHandler.sendMessage("request/planner","CallPlanner")
time.sleep(5)

stepsHandler = StepsHandler()
ledHandler = LEDHandler()

dbHandler = DBHandler(meas.returnMeas()[0],meas.returnMeas()[1],meas.returnMeas()[2],meas.returnMeas()[3],meas.returnMeas()[4])
dbHandler.openDB()
dbHandler.insertNewMeas()

if (stepsHandler.readOutputFile()):
	stepsHandler.findSteps()
	stepsHandler.dumpSteps()
	dbHandler.insertNewOutput(stepsHandler.getRadiator(),stepsHandler.getWindow(),stepsHandler.getBlinds(),stepsHandler.getLights())
	if (stepsHandler.getRadiator()!=""):
		if "CLOSE" in stepsHandler.getRadiator():
			ledHandler.radiatorLED(False)
		else:
			ledHandler.radiatorLED(True)
	else:
		ledHandler.radiatorLED(False)
	if (stepsHandler.getLights()!=""):
		if "TURNON" in stepsHandler.getLights():
			ledHandler.lightsLED(True)
		else:
			ledHandler.lightsLED(False)
	else:
		ledHandler.lightsLED(False)

	if (stepsHandler.getBlinds()!=""):
		if "CLOSE" in stepsHandler.getBlinds():
			ledHandler.blindsLED(False)
		else:
			ledHandler.blindsLED(True)
	else:
		ledHandler.blindsLED(False)

	if (stepsHandler.getWindow()!=""):
		if "CLOSE" in stepsHandler.getWindow():
			ledHandler.windowLED(False)
		else:
			ledHandler.windowLED(True)
	else:
		ledHandler.windowLED(False)


dbHandler.closeDB()
print(datetime.now().strftime("%Y-%m-%d | %H:%M:%S") + " -> Measurement Script Stopped") 


