(define (domain SmartCities)

 (:requirements :strips :typing)
 
   (:types 
      ProximitySensor TemperatureSensor 
      RadiatorActuator LightSensors LightActuator Windows Blinds - object 
   )

 (:predicates
     (MovementSensor ?mv - ProximitySensor)
    
     (LowTempClosedValve ?lt - TemperatureSensor ?cv - RadiatorActuator)
     (LowTempOpenValve ?lt - TemperatureSensor ?ov - RadiatorActuator)
     (CorrectTempClosedValve ?ct - TemperatureSensor ?cv - RadiatorActuator)
     (CorrectTempOpenValve ?ct - TemperatureSensor ?ov - RadiatorActuator)
     (HighTempClosedValve ?ht - TemperatureSensor ?cv - RadiatorActuator)
     (HighTempOpenValve ?ht - TemperatureSensor ?ov - RadiatorActuator)
     
     (OutsideHotterThanInside ?hot - TemperatureSensor)
     (OutsideColderThanInside ?cold - TemperatureSensor)
     
     (RoomWithOpenBlinds ?ob - Blinds)
     (RoomWithClosedBlinds ?cb - Blinds)
     
     (RoomWithLightsOn ?lo - LightActuator)
     (RoomWithLightsOff ?lof - LightActuator)

     (RoomWithRadiatorOn ?ro - RadiatorActuator)
     (RoomWithRadiatorOff ?roff - RadiatorActuator)
     
     (RoomWithOpenWindows ?ow - Windows)
     (RoomWithClosedWindows ?cw - Windows)

     (LowLightLightOff ?ll - LightSensors ?loff - LightActuator)
     (LowLightLightOn ?ll - LightSensors ?lon - LightActuator)
     (HighLightLightOff ?hl - LightSensors ?loff - LightActuator)
     (HighLightLightOn ?hl - LightSensors ?lon - LightActuator)

     (LowLightLevelOutside ?Outsidell - LightSensors)
     (HightLightLevelOutside ?Outsidehl - LightSensors)  
      
 )



(:action TurnOnLights
    :parameters 
    (?SomeoneInTheRoom - ProximitySensor
    ?LightSwitchOff ?LightSwitchOn - LightActuator
    ?LowLightLevel ?HighLightLevel - LightSensors)
    :precondition (and (LowLightLightOff ?LowLightLevel ?LightSwitchOff) (MovementSensor ?SomeoneInTheRoom) )
    :effect (and (HighLightLightOn ?HighLightLevel ?LightSwitchOn) (not(LowLightLightOff ?LowLightLevel ?LightSwitchOff))
))

(:action TurnOffLights
    :parameters 
    (?LightSwitchOff ?LightSwitchOn - LightActuator
    ?LowLightLevel ?HighLightLevel - LightSensors)
    :precondition (HighLightLightOn ?HighLightLevel ?LightSwitchOn)
    :effect (and (LowLightLightOff ?LowLightLevel ?LightSwitchOff) (not(HighLightLightOff ?HighLightLevel ?LightSwitchOn))
))


(:action OpenRadiatorValve
    :parameters 
    (?LowTemp ?HighTemp - TemperatureSensor 
    ?OpenValve ?ClosedValve - RadiatorActuator 
    ?SomeoneInTheRoom - ProximitySensor)
    :precondition (and (LowTempClosedValve ?LowTemp ?ClosedValve) (MovementSensor ?SomeoneInTheRoom))
    :effect (and (HighTempOpenValve ?HighTemp ?OpenValve) (not(LowTempClosedValve ?LowTemp ?ClosedValve)))
)

(:action OpenRadiatorValveMidDay
    :parameters 
    (?LowTemp ?CorrectTemp - TemperatureSensor 
    ?OpenValve ?ClosedValve - RadiatorActuator 
    ?SomeoneInTheRoom - ProximitySensor)
    :precondition (and (LowTempClosedValve ?LowTemp ?ClosedValve) (MovementSensor ?SomeoneInTheRoom))
    :effect (and (CorrectTempOpenValve ?CorrectTemp ?OpenValve) (not(LowTempClosedValve ?LowTemp ?ClosedValve)))
)

(:action CloseRadiatorValve
    :parameters 
    (?HighTemp ?LowTemp - TemperatureSensor 
    ?OpenValve ?ClosedValve - RadiatorActuator)
    :precondition  (HighTempOpenValve ?HighTemp ?OpenValve) 
    :effect (and (LowTempClosedValve ?LowTemp ?ClosedValve) (not(HighTempOpenValve ?HighTemp ?OpenValve)))
)

(:action CloseRadiatorValveMidDay
    :parameters 
    (?HighTemp ?CorrectTemp - TemperatureSensor 
    ?OpenValve ?ClosedValve - RadiatorActuator)
    :precondition (HighTempOpenValve ?HighTemp ?OpenValve)
    :effect (and (CorrectTempClosedValve ?CorrectTemp ?ClosedValve) (not(HighTempOpenValve ?HighTemp ?OpenValve)))
)


(:action OpenBlinds
    :parameters 
    (?BlindsUp ?BlindsDown - Blinds
    ?SomeoneInTheRoom - ProximitySensor)
    :precondition (and (MovementSensor ?SomeoneInTheRoom) (RoomWithClosedBlinds ?BlindsDown))
    :effect (and (RoomWithOpenBlinds ?BlindsUp) (not(RoomWithClosedBlinds ?BlindsDown)))
)

(:action CloseBlinds
    :parameters
    (?BlindsUp ?BlindsDown - Blinds)
    :precondition (RoomWithOpenBlinds ?BlindsUp)
    :effect (and (RoomWithClosedBlinds ?BlindsDown) (not(RoomWithOpenBlinds ?BlindsUp)))
)


(:action OpenWindows
    :parameters 
    (?WindowsOpen ?WindowsClosed - Windows
    ?OutsideHot - TemperatureSensor
    ?SomeoneInTheRoom - ProximitySensor)
    :precondition (and (MovementSensor ?SomeoneInTheRoom) (OutsideHotterThanInside ?OutsideHot) 
    (RoomWithClosedWindows ?WindowsClosed))
    :effect (and (RoomWithOpenWindows ?WindowsOpen) (not(RoomWithClosedWindows ?WindowsClosed)))
)

(:action CloseWindows
    :parameters 
    (?WindowsOpen ?WindowsClosed - Windows)
    :precondition (RoomWithOpenWindows ?WindowsOpen)
    :effect (and (RoomWithClosedWindows ?WindowsClosed) (not(RoomWithOpenWindows ?WindowsOpen)))
)


)