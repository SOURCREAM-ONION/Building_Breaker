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
        if self.y > 20:
            self.y -= 0.5

    def do(self):
        pass

    def get_bb(self):
        return self.x - 200, self.y - 15, self.x + 200, self.y + 325

    def draw(self):
        self.building.clip_draw(0, 307, 1080, 307, self.x, self.y, 400, 30)
        self.building.clip_draw(0, 614, 1080, 307, self.x, self.y + 35, 400, 30)
        self.building.clip_draw(0, 921, 1080, 307, self.x, self.y + 75, 400, 30)
        self.building.clip_draw(0, 1228, 1080, 307, self.x, self.y + 110, 400, 30)
        self.building.clip_draw(0, 1535, 1080, 307, self.x, self.y + 145, 400, 30)
        self.building.clip_draw(0, 1842, 1080, 307, self.x, self.y + 180, 400, 30)
        self.building.clip_draw(0, 2149, 1080, 307, self.x, self.y + 215, 400, 30)
        self.building.clip_draw(0, 2456, 1080, 307, self.x, self.y + 250, 400, 30)
        self.building.clip_draw(0, 2763, 1080, 307, self.x, self.y + 285, 400, 30)
        self.building.clip_draw(0, 3070, 1080, 307, self.x, self.y + 320, 400, 30)
        draw_rectangle(*self.get_bb())