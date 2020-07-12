(define (problem TooCold) (:domain SmartCities)
(:objects 
 LowTemperature HighTemperature - TemperatureSensor
 RadiatorValveClosed RadiatorValveOpen - RadiatorActuator
 SomeoneIntheRoom - ProximitySensor
 LowLightOutside LightsOnInside - LightSensors
 LightsOff LightsOn - LightActuator
 OpenWindows ClosedWindow - Windows
 BlindsClosed BlindsOpen - Blinds
)

(:init
    (MovementSensor SomeoneIntheRoom)
    (LowTempClosedValve LowTemperature RadiatorValveOpen)
)

(:goal 
    (CorrectTempOpenValve HighTemperature RadiatorValveOpen)
)

)
