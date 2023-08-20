# esc.py
class ESC:
    def __init__(self, max_current=30):
        self.max_current = max_current  # in A

    def control_speed(self, current):
        return f"Controlling motor speed with {current}A current"
