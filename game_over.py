from pico2d import *
import game_framework
import play_mode
import title_mode
import game_data
from coin import CoinBox

image = None
font_gameover = None
font_esc = None
font_score = None
font_coins = None

def init():
    global image, font_gameover, font_esc, font_score, font_coins, coin_box

    coin_box = CoinBox()
    image = load_image('background/EndBackground.png')
    font_gameover = load_font('ui/ENCR10B.ttf', 60)
    font_esc = load_font('ui/ENCR10B.ttf', 25)
    font_score = load_font('ui/ENCR10B.ttf', 30)
    font_coins = load_font('ui/ENCR10B.ttf', 25)

def finish():
    global image, font_gameover, font_esc, font_score, font_coins, coin_box

    del image
    del font_gameover
    del font_esc
    del font_score
    del font_coins
    del coin_box

def update():
    pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
            game_data.destroyed_buildings = 0 # 게임이 끝나면 파괴된 빌딩 수 초기화
            game_data.current_coin = 0 # 현재 코인 초기화

def draw():
    clear_canvas()
    image.draw_to_origin(0,0, 480, 720)
    font_gameover.draw(90, 530, 'Game Over', (255, 0, 0))
    font_esc.draw(115, 150, 'Press ESC to Title', (255, 255, 255))
    font_coins.draw(140, 460, f'Destroyed Building: {game_data.destroyed_buildings}', (255, 255, 255))
    font_score.draw(150, 390, f'Score: {int(play_mode.score)}', (255, 255, 255))
    font_coins.draw(140, 320, f'Collected Coins: {game_data.current_coin}', (255, 255, 255))
    coin_box.draw()

    update_canvas()