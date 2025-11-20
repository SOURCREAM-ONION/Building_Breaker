from pico2d import *
from state_machine import StateMachine
from character import Character, mouse_left_click, time_out, mouse_right_click, jump_key_press

import game_framework

class Idle_Sword:
    def __init__(self, sword):
        self.sword = sword
        self.frame = 0 # 검 대기 애니메이션 프레임 초기화

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        import math
        self.sword.image.clip_composite_draw(0, 0, 122, 122, -math.pi / 2, '' ,self.sword.x, self.sword.y, 50, 50)

class Wield_Sword:
    images = None

    def __init__(self, sword):
        self.y = 35
        self.sword = sword
        self.frame = 0
        self.frame_count = 6
        self.TIME_PER_ACTION = 1.0 / 0.09 # 검 휘두르기 애니메이션 속도
        self.ACTION_PER_TIME = 1.0 / 0.09 # 검 휘두르기 애니메이션 동작 시간
        self.FRAMES_PER_ACTION = 6 # 검 휘두르기 애니메이션 프레임 수

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time # 프레임을 시간처리
        if self.frame >= self.frame_count:
            self.sword.state_machine.handle_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.frame)
        if frame_index == 0:
            self.sword.image.clip_draw(0, 0, 204, 122, self.sword.x, self.y, 100, 50)
        elif frame_index == 1:
            self.sword.image.clip_draw(204, 0, 204, 122, self.sword.x, self.y, 100, 50)
        elif frame_index == 2:
            self.sword.image.clip_draw(408, 0, 204, 122, self.sword.x, self.y, 90, 50)
        elif frame_index == 3:
            self.sword.image.clip_draw(612, 0, 204, 122, self.sword.x, self.y, 90, 50)
        elif frame_index == 4:
            self.sword.image.clip_draw(816, 0, 204, 122, self.sword.x, self.y, 90, 50)
        elif frame_index == 5:
            self.sword.image.clip_draw(1020, 0, 204, 122, self.sword.x, self.y, 90, 50)

class Defence_Sword:
    def __init__(self, sword):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Sword:
    def __init__(self):
        self.x, self.y = 203, 27 # 검의 초기 위치
        self.image = load_image('basic_sword.png') # 검의 이미지 로드
        self.IDLE_SWORD = Idle_Sword(self)
        self.WIELD_SWORD = Wield_Sword(self)
        self.state_machine = StateMachine(
            self.IDLE_SWORD,
                    {
                        self.IDLE_SWORD: {mouse_left_click: self.WIELD_SWORD}, # IDLE상태일 때 일어나는 이벤트
                        self.WIELD_SWORD: {time_out : self.IDLE_SWORD}, # WIELD상태일 때 일어나는 이벤트
                    }
        )



    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        if self.state_machine.current_state == self.WIELD_SWORD: # 만약 검을 휘두르면
            draw_rectangle(*self.get_bb()) # 검의 충돌 박스 그리기 (실제 충돌처리와는 관련 X)

    def get_bb(self):
        return self.x - 40, self.y - 10, self.x + 40, self.y + 40

    def is_attacking(self):
        return self.state_machine.current_state == self.WIELD_SWORD

    def handle_event(self, event):
        pass
