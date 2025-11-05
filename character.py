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
        self.character.frame = (self.character.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 30, 120, 30, 30, 400, 300)

class Character:
    def __init__(self): # 캐릭터가 처음 생성될 때 나오는 부분
        self.x, self.y = 400, 300 # 캐릭터의 초기 위치
        self.frame = 0 # 캐릭터의 프레임 초기화
        self.image = load_image('Char1_1.png') # 캐릭터의 이미지 로드
        self.IDLE = Idle(self) # Idle 상태 생성
        self.state_machine = StateMachine(self.IDLE) #상태 머신 생성 및 초기 시작 상태 설정

    def update(self): # 캐릭터가 업데이트 되는 부분
        self.state_machine.update()

    def draw(self):  # 캐릭터가 그려지는 부분
        self.state_machine.draw()
        self.image.clip_draw(self.frame * 30, 30, 30, 30, 400, 300) # 캐릭터의 이미지에서 프레임에 맞게 그리기

