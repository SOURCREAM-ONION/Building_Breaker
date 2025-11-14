from pico2d import *

class Building:
    def __init__(self):
        self.x, self.y = 200, 500 # 건물의 초기 위치
        self.building = load_image('Building1.png')

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        if self.y > 200:
            self.y -= 0.5

    def do(self):
        pass

    def draw(self):
        self.building.draw_now(self.x, self.y, 400, 500)