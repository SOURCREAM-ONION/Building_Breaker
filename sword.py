from pico2d import *
from state_machine import StateMachine
from character import Character

class Sword:
    def __init__(self):
        self.x, self.y = 400, 90 # 검의 초기 위치
        self.image = load_image('basic_sword.png') # 검의 이미지 로드


    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

    def handle_event(self, event):
        pass
