from pico2d import load_image
from sdl2 import SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_KEYDOWN, SDLK_SPACE

from state_machine import StateMachine

def mouse_left_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT # 마우스 좌클릭
def time_out(e):
    return e[0] == 'TIME_OUT' # 애니메이션 끝나는 이벤트
def mouse_right_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_RIGHT # 마우스 우클릭
def jump_key_press(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE # 스페이스바 키 입력

class Idle:
    def __init__(self,character):
        self.character = character

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        self.character.frame = (self.character.frame + 1) % 4 # 프레임을 0~3까지 반복

    def draw(self):
        self.character.image.clip_draw(self.character.frame * 32, 95, 32, 35, 400, 90, 50, 50)

class Defence:
    def __init__ (self,character):
        self.character = character
        self.frame = 0 # 방어 애니메이션 프레임 초기화
        self.frame_count = 2 # 방어 애니메이션 프레임 수

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + 1 # 프레임을 1씩 증가
        if self.frame >= self.frame_count: # 프레임이 프레임 수보다 크거나 같으면
            # 이벤트를 발생시켜 상태 전환
            self.character.state_machine.handle_event(('TIME_OUT', None)) # 상태 전환

    def draw(self):
        if self.frame == 0: # 프레임이 0일때 재생
            self.character.image.clip_draw(128, 90, 32, 35, 400, 90, 50, 50)
        elif self.frame == 1: # 프레임이 1일때 재생
            self.character.image.clip_draw(0, 60, 32, 35, 400, 90, 50, 50)

class Jump:
    def __init__ (self,character):
        self.character = character
        self.frame = 0 # 점프 애니메이션 프레임 초기화
        self.frame_count = 3 # 점프 애니메이션 프레임 수

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + 1 # 프레임을 1씩 증가
        if self.frame >= self.frame_count:
            # 이벤트를 발생시켜 상태 전환
            self.character.state_machine.handle_event(('TIME_OUT', None))

    def draw(self):
        if self.frame == 0: # 0번 프레임 재생
            self.character.image.clip_draw(32, 60, 32, 35, 400, 90, 50, 50)
        elif self.frame == 1: # 1번 프레임 재생
            self.character.image.clip_draw(64, 60, 32, 35, 400, 90, 50, 50)
        elif self.frame == 2: # 2번 프레임 재생
            self.character.image.clip_draw(96, 60, 32, 35, 400, 90, 50, 50)

class Attack:
    def __init__ (self,character):
        self.character = character
        self.frame = 0
        self.frame_count = 4

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + 1
        if self.frame >= self.frame_count:
            # 이벤트를 발생시켜 상태 전환
            self.character.state_machine.handle_event(('TIME_OUT', None))

    def draw(self):
        # 현재 프레임에 해당하는 이미지만 그리기
        if self.frame == 0:
            self.character.image.clip_draw(128, 60, 32, 35, 400, 90, 50, 50)
        elif self.frame == 1:
            self.character.image.clip_draw(0, 29, 32, 35, 400, 90, 50, 50)
        elif self.frame == 2:
            self.character.image.clip_draw(32, 29, 32, 35, 400, 90, 50, 50)
        elif self.frame == 3:
            self.character.image.clip_draw(64, 29, 32, 35, 400, 90, 50, 50)

class Character:
    def __init__(self): # 캐릭터가 처음 생성될 때 나오는 부분
        self.x, self.y = 400, 300 # 캐릭터의 초기 위치
        self.frame = 0 # 캐릭터의 프레임 초기화
        self.image = load_image('Char1_1.png') # 캐릭터의 이미지 로드
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

    def update(self):
        self.state_machine.update()  # 상태 머신한테 update를 맡김

    def draw(self):  # 캐릭터가 그려지는 부분
        self.state_machine.draw() # 상태 머신한테 draw를 맡김

    def handle_event(self, event): # 이벤트가 발생했을 때 처리하는 부분
        self.state_machine.handle_event(('INPUT', event)) # 상태 머신한테 이벤트 처리를 맡김
