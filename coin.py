from pico2d import *
import random
import game_data
import play_mode

# 동전 클래스
class Coin:
    image = None

    def __init__(self,x = None):
        if Coin.image is None:
            Coin.image = load_image('ui/coin.png')
        self.x = x if x is not None else random.randint(50, 600) # 동전의 x 좌표를 무작위로 설정
        self.y = 80 # 동전의 y 좌표 초기값 설정
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
        screen_y = self.y - play_mode.camera_y # 카메라 위치에 따른 y 좌표 계산
        self.image.clip_draw(self.frame * 1067, 0, 1067, 1067, self.x, screen_y, 100, 100) # 동전 그리기 (캐릭터가 위로 올라가도 동전은 그대로)
        # draw_rectangle(self.x - 20, screen_y - 20, self.x + 20, screen_y + 20)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

# 동전 UI 클래스
class CoinBox:
    def __init__(self):
        self.image = load_image("ui/coinbox.png")

        self.font = load_font('ui/ENCR10B.ttf', 30)
        self.x = 380
        self.y = 680

    def draw(self):
        self.image.draw(self.x, self.y, 200, 65)
        self.font.draw(self.x - 20 , self.y, f'{game_data.total_coins}', (50, 50, 50))