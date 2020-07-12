(define (problem TimeToGoHome_WindowsOpen_RadiatorOpen) (:domain SmartCities)
(:objects 
 LowTemperature HighTemperature - TemperatureSensor
 RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
 LowLightLevel HighLightLevel - LightSensors
 LightsOff LightsOn - LightActuator
 BlindsClosed BlindsOpen - Blinds
 WindowsOpen WindowsClosed - Windows
 SomeoneInTheRoom NobodyInTheRoom - ProximitySensor
)

(:init
(RoomWithOpenBlinds BlindsOpen)
(HighTempOpenValve HighTemperature RadiatorValveOpen)
(HighLightLightOn HighLightLevel LightsOn)
(RoomWithOpenWindows WindowsOpen)
)

(:goal
(and 
(LowTempClosedValve LowTemperature RadiatorValveClosed)
(LowLightLightOff LowLightLevel LightsOff)
(RoomWithClosedBlinds BlindsClosed)
(RoomWithClosedWindows WindowsClosed)
)
)
)
