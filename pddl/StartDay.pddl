(define (problem ColdAndDarkRoom) (:domain SmartCities)
(:objects 
 LowTemperature HighTemperature - TemperatureSensor
 RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
 SomeoneInTheRoom NobodyInTheRoom - ProximitySensor
 LowLightLevel HighLightLevel - LightSensors
 LightsOff LightsOn - LightActuator
 BlindsClosed BlindsOpen - Blinds
 OpenWindows ClosedWindow - Windows
)

(:init
(MovementSensor SomeoneInTheRoom)
(RoomWithClosedBlinds BlindsClosed)
(LowTempClosedValve LowTemperature RadiatorValveClosed)
(LowLightLightOff LowLightLevel LightsOff)
)

(:goal
(and 
(HighTempOpenValve HighTemperature RadiatorValveOpen)
(HighLightLightOn HighLightLevel LightsOn)
(RoomWithOpenBlinds BlindsOpen)
)
)
)
