from pico2d import *
import random

class Coin:
    image = None

    def __init__(self, x = None, y = 80):
        if Coin.image is None:
            Coin.image = load_image('ui/coin.png')
        self.x = x if x is not None else random.randint(20, 700)
        self.y = y
        self.frame = 0
        self.total_frames = 4
        self.animation_speed = 30
        self.delay_counter = 0

    def update(self):
        self.delay_counter += 1
        if self.delay_counter >= self.animation_speed:
            self.frame = (self.frame + 1) % self.total_frames
            self.delay_counter = 0

    def draw(self):
        self.image.clip_draw(self.frame * 1067, 0, 1067, 1067, self.x, self.y, 100, 100)