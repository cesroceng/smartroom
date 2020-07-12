(define (problem TimeToGoHome) (:domain SmartCities)
(:objects 
 LowTemperature HighTemperature - TemperatureSensor
 RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
 LowLightLevel HighLightLevel - LightSensors
 LightsOff LightsOn - LightActuator
 BlindsClosed BlindsOpen - Blinds
 OpenWindows ClosedWindow - Windows
 SomeoneInTheRoom NobodyInTheRoom - ProximitySensor
)

(:init
(RoomWithOpenBlinds BlindsOpen)
(HighTempOpenValve HighTemperature RadiatorValveOpen)
(HighLightLightOn HighLightLevel LightsOn)
)

(:goal
(and 
(LowTempClosedValve LowTemperature RadiatorValveClosed)
(LowLightLightOff LowLightLevel LightsOff)
(RoomWithClosedBlinds BlindsClosed)
)
)
)
