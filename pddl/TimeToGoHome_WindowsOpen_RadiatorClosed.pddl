(define (problem TimeToGoHome_WindowsOpen_RadiatorClosed) (:domain SmartCities)
(:objects 
 LowTemperature HighTemperature - TemperatureSensor
 LowLightLevel HighLightLevel - LightSensors
 LightsOff LightsOn - LightActuator
 BlindsClosed BlindsOpen - Blinds
 WindowsOpen WindowsClosed - Windows
 RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
 SomeoneInTheRoom NobodyInTheRoom - ProximitySensor
)

(:init
(RoomWithOpenBlinds BlindsOpen)
(HighLightLightOn HighLightLevel LightsOn)
(RoomWithOpenWindows WindowsOpen)
)

(:goal
(and 
(LowLightLightOff LowLightLevel LightsOff)
(RoomWithClosedBlinds BlindsClosed)
(RoomWithClosedWindows WindowsClosed)
)
)
)
