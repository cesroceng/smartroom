(define (problem FreeHeating) (:domain SmartCities)
(:objects 
    SomeoneInTheRoom - ProximitySensor
    HighTemperatureOutside LowTemperatureOutside - TemperatureSensor
    OpenWindows ClosedWindow - Windows
    LowLightLevel HighLightLevel - LightSensors
    LightsOff LightsOn - LightActuator
    RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
    BlindsClosed BlindsOpen - Blinds
)

(:init
 (MovementSensor SomeoneInTheRoom)
 (OutsideHotterThanInside HighTemperatureOutside)
 (RoomWithClosedWindows ClosedWindow)
)

(:goal (and
(RoomWithOpenWindows OpenWindows)    
))
)
