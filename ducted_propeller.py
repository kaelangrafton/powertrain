# ducted_propeller.py
import math

class DuctedPropeller:
    def __init__(self, propeller_diameter, hub_diameter, air_density, diffuser_expansion_ratio, correction_factor):
        self.propeller_diameter = propeller_diameter
        self.hub_diameter = hub_diameter
        self.air_density = air_density
        self.diffuser_expansion_ratio = diffuser_expansion_ratio
        self.correction_factor = correction_factor

    def rotor_area(self):
        """Calculate the rotor area based on the annulus formed by the propeller and hub diameters."""
        outer_area = math.pi * (self.propeller_diameter / 2)**2
        inner_area = math.pi * (self.hub_diameter / 2)**2
        return outer_area - inner_area

    def static_thrust(self, motor):
        """Calculate the static thrust using the provided formula."""
        power = motor.motor_power  # Retrieve power from the motor object
        thrust = self.correction_factor * (self.air_density * self.rotor_area() / self.diffuser_expansion_ratio)**(1/3) * power**(2/3)
        return thrust