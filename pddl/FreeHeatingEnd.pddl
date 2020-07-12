(define (problem FreeHeatingEnd) (:domain SmartCities)
(:objects 
    LowTemperatureOutside - TemperatureSensor
    OpenWindows ClosedWindow - Windows
    LowLightLevel HighLightLevel - LightSensors
    LightsOff LightsOn - LightActuator
    RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
    BlindsClosed BlindsOpen - Blinds
    SomeoneInTheRoom NobodyInTheRoom - ProximitySensor
)

(:init
 (OutsideColderThanInside LowTemperatureOutside)
 (RoomWithOpenWindows OpenWindows)
)

(:goal 
(RoomWithClosedWindows ClosedWindow)    
)

)
