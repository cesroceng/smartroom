(define (problem TimeToGoHome_WindowsClosed_RadiatorClosed) (:domain SmartCities)
(:objects 
 LowTemperature HighTemperature - TemperatureSensor
 SomeoneInTheRoom - ProximitySensor
 LowLightLevel HighLightLevel - LightSensors
 LightsOff LightsOn - LightActuator
 BlindsClosed BlindsOpen - Blinds
 OpenWindows ClosedWindow - Windows
 RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
)

(:init
(MovementSensor SomeoneInTheRoom)
(RoomWithOpenBlinds BlindsOpen)
(HighLightLightOn HighLightLevel LightsOn)
)

(:goal
(and 
(LowLightLightOff LowLightLevel LightsOff)
(RoomWithClosedBlinds BlindsClosed)
)
)
)
