class StateMachine:
    def __init__(self, start_state):
        self.current_state = start_state
        self.current_state.enter()

    def update(self):
        self.current_state.do() # 현재 상태의 do 메서드 호출

    def draw(self):
        self.current_state.draw() # 현재 상태의 draw 메서드 호출
