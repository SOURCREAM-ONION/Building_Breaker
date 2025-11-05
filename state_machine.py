class StateMachine:
    def __init__(self, start_state):
        self.current_state = start_state
        self.current_state.enter()

    def update(self):
        self.current_state.do()
