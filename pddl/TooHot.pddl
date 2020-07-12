(define (problem RoomTooHot) (:domain SmartCities)
(:objects 
 CorrectTemperature HighTemperature - TemperatureSensor
 RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
 LowLightOutside LightsOnInside - LightSensors
 LightsOff LightsOn - LightActuator
 OpenWindows ClosedWindow - Windows
 BlindsClosed BlindsOpen - Blinds
 SomeoneInTheRoom NobodyInTheRoom - ProximitySensor
)

(:init
    (HighTempOpenValve HighTemperature RadiatorValveOpen)
)

(:goal (and 
(CorrectTempClosedValve CorrectTemperature RadiatorValveClosed)
(not(HighTempOpenValve HighTemperature RadiatorValveOpen))
)
)


)

