#!/usr/bin/env python
import paho.mqtt.client as mqtt
import os
from multiprocessing import Process

DECISION_TOPIC = "request/decision"
PLANNER_TOPIC = "request/planner"

MIN_TEMP = 27
MAX_TEMP = 33
TRIGGER_DARK = 7000

class Subscriber:
	def __init__(self):
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.temp1 = ""
		self.temp2 = ""
		self.light1 = ""
		self.light2 = ""
		self.motion = ""
		self.pddlFile = None
	        self.radiatorClosed = True
        	self.windowsClosed = True
	        self.lightsOff = True
        	self.blindsClosed = True

	def on_connect(self,client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		self.client.subscribe("request/#")

	def on_message(self,client, userdata, msg):
		if (msg.topic==DECISION_TOPIC):
			print(msg.topic+" "+str(msg.payload))
			list = str(msg.payload).split(";")
			self.temp1 = list[0]
			self.temp2 = list[1]
			self.light1 = list[2]
			self.light2 = list[3]
			self.motion = list[4]
			self.takeDecision()
		if (msg.topic==PLANNER_TOPIC):
			print(msg.topic+" "+str(msg.payload))
			self.callPlanner()

	def myConnect(self):
		self.client.connect("localhost",1883,60)
		self.client.loop_forever()

	def takeDecision(self):
		if ((float(self.temp1) < MIN_TEMP) and (float(self.light1) > TRIGGER_DARK) and (int(self.motion) == 1) and (self.radiatorClosed == True) and (self.lightsOff == True) and (self.blindsClosed == True) and (self.windowsClosed == True)):
			self.pddlFile = "StartDay.pddl"
			self.radiatorClosed = False
		        self.lightsOff = False
		        self.blindsClosed = False
		elif (float(self.temp1) > MAX_TEMP) and (self.radiatorClosed == False):
			self.pddlFile = "TooHot.pddl"
		        self.radiatorClosed = True
		elif (float(self.temp1) < MIN_TEMP) and (self.radiatorClosed == True) and (int(self.motion) == 1):
			self.pddlFile = "TooCold.pddl"
		        self.radiatorClosed = True
		elif (float(self.temp1)< MIN_TEMP) and (float(self.temp1) < float(self.temp2)) and (int(self.motion) == 1) and (self.windowsClosed == True):
		        self.pddlFile = "FreeHeating.pddl"
		        self.windowsClosed = False
		elif (float(self.temp2) < float(self.temp1)) and (self.windowsClosed == False):
		        self.pddlFile = "FreeHeatingEnd.pddl"
		        self.windowsClosed = True
		elif (int(self.motion) == 0) and (self.radiatorClosed == True) and (self.windowsClosed == True):
		        self.pddlFile = "TimeToGoHome_WindowsClosed_RadiatorClosed.pddl"
		        self.lightsOff = True
		        self.blindsClosed = True
		elif (int(self.motion) == 0) and (self.radiatorClosed == False) and (self.windowsClosed == True):
		        self.pddlFile = "TimeToGoHome_WindowsClosed_RadiatorOpen.pddl"
		        self.radiatorClosed = True
		        self.lightsOff = True
		        self.blindsClosed = True
		elif (int(self.motion) == 0) and (self.radiatorClosed == True) and (self.windowsClosed == False):
		        self.pddlFile = "TimeToGoHome_WindowsOpen_RadiatorClosed.pddl"
		        self.windowsClosed = True
		        self.lightsOff = True
		        self.blindsClosed = True
		elif (int(self.motion) == 0) and (self.radiatorClosed == False) and (self.windowsClosed == False):
			self.pddlFile = "TimeToGoHome_WindowsOpen_RadiatorOpen.pddl"
		        self.radiatorClosed = True
		        self.windowsClosed = True
		        self.lightsOff = True
		        self.blindsClosed = True

		print(self.pddlFile)

	def callPlanner(self):
		os.system("./../FF-v2.3/ff -o pddl/domain.pddl -f pddl/"+self.pddlFile+" > Output.txt")
		print("Plan found and saved!")

subscriberHandler = Subscriber()
subscriberHandler.myConnect()
