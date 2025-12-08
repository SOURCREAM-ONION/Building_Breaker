from pico2d import *
import game_framework
import play_mode
import title_mode
import select_character
from background import (Background2, Background3, Background4, Background5, Background6, Background7, Background8, Background9, Background10, Background11, Background12,
                        Background13, Background14, Background15, Background16, Background17, Background18, Background19, Background20, Background21, Background22, Background23,
                        Background24, Background25, Background26, Background27, Background28, Background29, Background30, Background31, Background32, Background33, Background34, Background35, Background36)

import game_data
from coin import CoinBox


direction_image = None

def init():
    global map_list, direction_image, current_preview, selection_index # 맵 선택 관련 글로벌 변수
    global coin_box, map_prices, unlock_status, font_unlock # 상점 관련 글로벌 변수

    coin_box = CoinBox()

    map_list = [Background2, Background3, Background4, Background5, Background6, Background7, Background8, Background9, Background10,
                Background11, Background12, Background13, Background14, Background15, Background16, Background17, Background18, Background19,
                Background20, Background21, Background22, Background23, Background24, Background25, Background26, Background27, Background28,
                Background29, Background30, Background31, Background32, Background33, Background34, Background35, Background36]

    selection_index = 0
    current_preview = map_list[selection_index]()
    direction_image = load_image("ui/Direction_21.png")
    font_unlock = load_font("ui/ENCR10B.TTF", 20)

    map_prices = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                  ,1, 1, 1, 1, 1]

    # 해금상태 초기와 = 기본 맵 해금
    unlock_status = []
    for price in map_prices:
        if price == 0:
            unlock_status.append(True)
        else:
            unlock_status.append(False)

def finish():
    global current_preview
    global direction_image
    global font_unlock

    del current_preview
    del direction_image
    del font_unlock

def update():
    pass

def draw():
    clear_canvas()

    current_preview.image.draw(240, 360, 480, 720)
    if direction_image:
        direction_image.draw(430, 360, 100, 100)
        direction_image.composite_draw(0, 'h', 50, 360, 100, 100)

    coin_box.draw()

    # 맵이 잠겼을 때 나오는 문구
    if not unlock_status[selection_index]:
        font_unlock.draw(140, 600, "LOCKED", (255, 0, 0))
        font_unlock.draw(120, 550, f"{map_prices[selection_index]} Coin", (255, 255, 255))

    update_canvas()

def handle_events():
    global selection_index, current_preview

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(title_mode)
            elif event.key == SDLK_LEFT: # 왼쪽 화살표 키 입력
                selection_index = (selection_index - 1) % len(map_list)
                direction_image.composite_draw(0, 'h', 60, 360, 120, 120)
                update_canvas()
                del current_preview
                current_preview = map_list[selection_index]()
            elif event.key == SDLK_RIGHT: # 오른쪽 화살표 키 입력
                selection_index = (selection_index + 1) % len(map_list)
                direction_image.draw(420, 360, 120, 120)
                update_canvas()
                del current_preview
                current_preview = map_list[selection_index]()
            elif event.key == SDLK_SPACE:
                if unlock_status[selection_index]: # 잠금 해제된 맵일 때 게임실행
                    selected_class = map_list[selection_index]
                    select_character.set_background(selected_class)
                    play_mode.set_background_class(selected_class)
                    game_framework.change_mode(select_character)
                else:
                    price = map_prices[selection_index]
                    if game_data.current_coin >= price:
                        game_data.current_coin -= price
                        unlock_status[selection_index] = True
                        print(f'Map {selection_index} unlocked!')
                    else:
                        print('Not enough coins to unlock this map.')