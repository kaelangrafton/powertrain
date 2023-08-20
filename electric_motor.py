# electric_motor.py
class ElectricMotor:
    def __init__(self, motor_power, rpm=10000):
        self.motor_power = motor_power  # in W
        self.rpm = rpm

    def rotate(self):
        return f"Rotating at {self.rpm} RPM"
