# lithium_ion_battery.py
class LithiumIonBattery:
    def __init__(self, mass, specific_energy, voltage=3.7):
        self.mass = mass  # in kg
        self.specific_energy = specific_energy  # in Wh/kg
        self.voltage = voltage  # in V

    def charge(self):
        return f"Charging the battery to {self.capacity()}mAh"

    def discharge(self):
        return f"Discharging the battery at {self.voltage}V"

    def capacity(self):
        return self.mass * self.specific_energy  # Total energy in Wh

    def runtime(self, motor):
            return self.capacity() / motor.motor_power  # Total runtime in hours
