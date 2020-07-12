(define (problem OvercastDay) (:domain SmartCities)
(:objects 
LowTemperature CorrectTemperature HighTemperature - TemperatureSensor
RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
SomeoneInTheRoom NobodyInTheRoom - ProximitySensor
LowLightOutside LightsOnInside - LightSensors
LightsOff LightsOn - LightActuator
BlindsClosed BlindsOpen - Blinds
)

(:init
    (RoomWithOpenBlinds BlindsOpen)
    (LowLightLevelOutside LowLightOutSide)
)

(:goal (and
    (RoomWithClosedBlinds BlindsClosed)
   
    (not(RoomWithOpenBlinds BlindsOpen))
)
)
)
