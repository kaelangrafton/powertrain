class Powertrain:
    def __init__(self, battery, motor):
        self.battery = battery
        self.motor = motor
        self.capacity_history = [battery.capacity()]  # Initialize with the full battery capacity
        self.runtime = None  # Initialize runtime attribute

    def simulate(self, time_step=1):
        """Simulate the powertrain operation over time."""
        self.runtime = self.battery.runtime(self.motor)
        time = 0

        while time < self.runtime:
            time += time_step
            remaining_capacity = self.capacity_history[-1] - self.motor.motor_power * time_step
            self.capacity_history.append(remaining_capacity)

    def get_time_history(self):
        """Return the time history of the simulation."""
        return [i for i in range(len(self.capacity_history))]
