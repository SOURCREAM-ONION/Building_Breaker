from pico2d import load_image
from state_machine import StateMachine


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

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        self.character.image.clip_draw(128, 65, 32, 35, 400, 90, 50, 50)
        self.character.image.clip_draw(0, 35, 32, 35, 400, 90, 50, 50)
        self.character.image.clip_draw(32, 35, 32, 35, 400, 90, 50, 50)
        self.character.image.clip_draw(64, 35, 32, 35, 400, 90, 50, 50)

class Character:
    def __init__(self): # 캐릭터가 처음 생성될 때 나오는 부분
        self.x, self.y = 400, 300 # 캐릭터의 초기 위치
        self.frame = 0 # 캐릭터의 프레임 초기화
        self.image = load_image('Char1_1.png') # 캐릭터의 이미지 로드
        self.IDLE = Idle(self) # Idle 상태 생성
        self.state_machine = StateMachine(self.IDLE) #상태 머신 생성 및 초기 시작 상태 설정 (Idle로 초기 설정)

    def update(self):
        self.state_machine.update() # 상태 머신한테 update를 맡김

    def draw(self):  # 캐릭터가 그려지는 부분
        self.state_machine.draw() # 상태 머신한테 draw를 맡김

