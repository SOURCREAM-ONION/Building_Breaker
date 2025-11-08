from pico2d import load_image
from sdl2 import SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

from state_machine import StateMachine

def mouse_left_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT # 마우스 좌클릭

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
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass

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
        self.frame = (self.frame + 1) % self.frame_count  # 프레임을 0~3까지 반복

    def draw(self):
        # 현재 프레임에 해당하는 이미지만 그리기
        if self.frame == 0:
            self.character.image.clip_draw(128, 65, 32, 35, 400, 90, 50, 50)
        elif self.frame == 1:
            self.character.image.clip_draw(0, 35, 32, 35, 400, 90, 50, 50)
        elif self.frame == 2:
            self.character.image.clip_draw(32, 35, 32, 35, 400, 90, 50, 50)
        elif self.frame == 3:
            self.character.image.clip_draw(64, 35, 32, 35, 400, 90, 50, 50)

class Character:
    def __init__(self): # 캐릭터가 처음 생성될 때 나오는 부분
        self.x, self.y = 400, 300 # 캐릭터의 초기 위치
        self.frame = 0 # 캐릭터의 프레임 초기화
        self.image = load_image('Char1_1.png') # 캐릭터의 이미지 로드
        self.IDLE = Idle(self) # Idle 상태 생성
        self.ATTACK = Attack(self) # Attack 상태 생성
        self.DEFENCE = Defence(self) # Defence 상태 생성
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {mouse_left_click : self.ATTACK}
            }
        )

    def update(self):
        self.state_machine.update()  # 상태 머신한테 update를 맡김

    def draw(self):  # 캐릭터가 그려지는 부분
        self.state_machine.draw() # 상태 머신한테 draw를 맡김

    def handle_event(self, event): # 이벤트가 발생했을 때 처리하는 부분
        self.state_machine.handle_event(('INPUT', event)) # 상태 머신한테 이벤트 처리를 맡김
