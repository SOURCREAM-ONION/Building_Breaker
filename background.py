from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image("Background_04_03.png")


    def update(self):
        pass

    def draw(self):
        self.image.draw(240, 360, 480, 720)