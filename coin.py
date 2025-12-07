from pico2d import *
import random
import game_data

class Coin:
    image = None

    def __init__(self,x = None):
        if Coin.image is None:
            Coin.image = load_image('ui/coin.png')
        self.x = x if x is not None else random.randint(50, 600)
        self.y = 80
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
        draw_rectangle(* self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20


class CoinBox:
    def __init__(self):
        self.image = load_image("ui/coinbox.png")

        self.font = load_font('ui/ENCR10B.ttf', 30)
        self.x = 380
        self.y = 680

    def draw(self):
        # 상자 그리기
        self.image.draw(self.x, self.y, 200, 65)
        self.font.draw(self.x - 20 , self.y, f'{game_data.total_coins}', (50, 50, 50))