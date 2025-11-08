class StateMachine:
    def __init__(self, start_state, transitions = None):
        self.current_state = start_state # 초기 상태를 시작상태로 설정
        self.transitions = transitions if transitions else {}
        self.current_state.enter() # 시작 상태

    def update(self):
        self.current_state.do() # 현재 상태를 계속 실행

    def draw(self):
        self.current_state.draw() # 현재 상태의 draw 메서드 호출

    def handle_event(self, event):
        for event_check in self.transitions.get(self.current_state, {}):
            if event_check(event): # 이벤트가 해당 상태의 전이 조건과 일치하는지 확인
                next_state = self.transitions[self.current_state][event_check]
                self.current_state.exit() # 현재 상태 종료
                next_state.enter() # 다음 상태 진입
                print(f'State Change: {self.current_state.__class__.__name__} ======= {event} ======= {next_state.__class__.__name__}')
                self.current_state = next_state # 상태 전환
                return
        print(f'Unhandled event {event} in state {self.current_state.__class__.__name__}')