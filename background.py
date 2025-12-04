from pico2d import *

class Background:
    def __init__(self, image_name):
        self.image = load_image(image_name)


    def update(self):
        pass

    def draw(self):
        self.image.draw(240, 360, 480, 720)


class Background2(Background):
    def __init__(self):
        super().__init__ ("Background_04_03.png") # 야자수 배경

class Background3(Background):
    def __init__(self):
        super().__init__ ("Background_06_02.png") # 흐릿한 도시 배경

