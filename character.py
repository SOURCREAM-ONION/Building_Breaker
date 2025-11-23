from pico2d import load_image
from sdl2 import SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_KEYDOWN, SDLK_SPACE
from state_machine import StateMachine

import game_framework
import game_world

def mouse_left_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT # 마우스 좌클릭
def time_out(e):
    return e[0] == 'TIME_OUT' # 애니메이션 끝나는 이벤트
def mouse_right_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_RIGHT # 마우스 우클릭
def jump_key_press(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE # 스페이스바 키 입력

# 캐릭터의 시간변수
# IDLE상태와 DEFENCE상태에서 공통으로 사용 (점프와 공격은 별도 처리)
TIME_PER_ACTION = 0.5 # 한 동작에 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 초당 동작 수
FRAMES_PER_ACTION = 4 # 동작당 프레임 수

class Idle:
    def __init__(self,character):
        self.character = character
        self.y = character.y

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        self.character.frame = (self.character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4 # 프레임을 0~3까지 반복

    def draw(self):
        frame_index = int(self.character.frame)
        self.character.image.clip_draw(frame_index * 32, 95, 32, 35, 200, self.y, 50, 50)

class Defence:
    def __init__ (self,character):
        self.character = character
        self.y = character.y
        self.frame = 0 # 방어 애니메이션 프레임 초기화
        self.frame_count = 2 # 방어 애니메이션 프레임 수

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time # 프레임을 1씩 증가
        if self.frame >= self.frame_count: # 프레임이 프레임 수보다 크거나 같으면
            # 이벤트를 발생시켜 상태 전환
            self.character.state_machine.handle_event(('TIME_OUT', None)) # 상태 전환

    def draw(self):
        frame_index = int(self.frame)
        if frame_index == 0:
            self.character.image.clip_draw(128, 93, 32, 35, 200, self.y, 50, 50)
        elif frame_index == 1:
            self.character.image.clip_draw(0, 61, 32, 35, 200, self.y, 50, 50)

class Jump:
    FRAMES_PER_ACTION = 3 # 점프 애니메이션 프레임 수
    ACTION_PER_TIME = 1.0 / 0.2 # 점프 애니메이션 속도 (0.1초에 한 번 동작)

    def __init__ (self,character):
        self.character = character
        self.y = character.y
        self.frame = 0 # 점프 애니메이션 프레임 초기화
        self.frame_count = 3 # 점프 애니메이션 프레임 수

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time # 프레임을 시간처리
        if self.frame >= self.frame_count:
            # 이벤트를 발생시켜 상태 전환
            self.character.state_machine.handle_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.frame)
        if frame_index == 0:
            self.character.image.clip_draw(32, 60, 32, 35, 200, self.y, 50, 50)
        elif frame_index == 1:
            self.character.image.clip_draw(64, 61, 32, 35, 200, self.y, 50, 50)
        elif frame_index == 2:
            self.character.image.clip_draw(96, 61, 32, 35, 200, self.y, 50, 50)

class Attack:
    FRAMES_PER_ACTION = 3 # 공격 애니메이션 프레임 수
    ACTION_PER_TIME = 1.0 / 0.1 # 공격 애니메이션 속도 (0.1초에 한 번 동작)

    def __init__ (self,character):
        self.character = character
        self.y = character.y
        self.frame = 0
        self.frame_count = 3

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time # 프레임을 시간처리
        if self.frame >= self.frame_count:
            # 이벤트를 발생시켜 상태 전환
            self.character.state_machine.handle_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.frame)
        if frame_index == 0:
            self.character.image.clip_draw(0, 29, 32, 35, 200, self.y, 50, 50)
        elif frame_index == 1:
            self.character.image.clip_draw(32, 29, 32, 35, 200, self.y, 50, 50)
        elif frame_index == 2:
            self.character.image.clip_draw(64, 29, 32, 35, 200, self.y, 50, 50)

class Character:
    def __init__(self): # 캐릭터가 처음 생성될 때 나오는 부분
        self.x, self.y = 200, 30 # 캐릭터의 초기 위치
        self.frame = 0 # 캐릭터의 프레임 초기화
        self.image = load_image('Char1_1.png') # 캐릭터의 이미지 로드
        self.last_defence_time = 0.0 # 마지막 방어 시간 초기화
        self.defence_cooltime = 2.0 # 방어 쿨타임 설정 (초단위)

        self.IDLE = Idle(self) # Idle 상태 생성
        self.ATTACK = Attack(self) # Attack 상태 생성
        self.DEFENCE = Defence(self) # Defence 상태 생성
        self.JUMP = Jump(self) # Jump 상태 생성
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {mouse_left_click : self.ATTACK, mouse_right_click : self.DEFENCE, jump_key_press : self.JUMP},
                self.ATTACK : {time_out : self.IDLE},
                self.DEFENCE : {time_out : self.IDLE},
                self.JUMP : {time_out : self.IDLE},
            }
        )

    def can_defence(self):
        import time
        current_time = time.time()
        if current_time - self.last_defence_time >= self.defence_cooltime:
            self.last_defence_time = current_time
            return True
        return False

    def update(self):
        self.state_machine.update()  # 상태 머신한테 update를 맡김

    def draw(self):  # 캐릭터가 그려지는 부분
        self.state_machine.draw() # 상태 머신한테 draw를 맡김

    def handle_event(self, event): # 이벤트가 발생했을 때 처리하는 부분
        # 방어 입력 시 쿨다운 체크
        if mouse_right_click(('INPUT', event)):
            if self.can_defence():
                self.state_machine.handle_event(('INPUT', event))
        else:
            self.state_machine.handle_event(('INPUT', event))
