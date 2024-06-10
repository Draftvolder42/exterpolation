
class ButtonMode:
    def __init__(self):
        self.lock = False
        self.lock2 = False
        self.mem = False
        self.mem2 = False

    def toggle_to_push(self, state):
        if not state:
            self.lock = False
        if state and not self.lock:
            self.lock = True
            return True

    def push_to_toggle(self, state):
        self.mem = False
        if not state:
            self.lock2 = False
        if state and not self.lock2:
            self.lock2 = True
            self.mem = True
        if self.mem and self.mem2:
            self.mem2 = False
        elif self.mem:
            self.mem2 = True
        return self.mem2