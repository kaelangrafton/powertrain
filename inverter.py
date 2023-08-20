# inverter.py
class Inverter:
    def __init__(self, efficiency=0.95):
        self.efficiency = efficiency

    def convert(self):
        return f"Converting DC to AC with {self.efficiency * 100}% efficiency"
