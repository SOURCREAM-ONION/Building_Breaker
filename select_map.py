from pico2d import *
import game_framework
import play_mode
import title_mode
import select_character
from background import (Background2, Background3, Background4, Background5, Background6, Background7, Background8, Background9, Background10, Background11, Background12,
                        Background13, Background14, Background15, Background16, Background17, Background18, Background19, Background20, Background21, Background22, Background23,
                        Background24, Background25, Background26, Background27, Background28, Background29, Background30, Background31, Background32, Background33, Background34, Background35, Background36)

import game_data
direction_image = None

def init():
    global map_list
    global selection_index
    global current_preview
    global direction_image

    map_list = [Background2, Background3, Background4, Background5, Background6, Background7, Background8, Background9, Background10,
                Background11, Background12, Background13, Background14, Background15, Background16, Background17, Background18, Background19,
                Background20, Background21, Background22, Background23, Background24, Background25, Background26, Background27, Background28,
                Background29, Background30, Background31, Background32, Background33, Background34, Background35, Background36]
    selection_index = 0

    current_preview = map_list[selection_index]()

    direction_image = load_image("ui/Direction_21.png")

def finish():
    global current_preview
    global direction_image

    del current_preview
    del direction_image

def update():
    pass

def draw():
    clear_canvas()

    current_preview.draw()
    if direction_image:
        direction_image.draw(430, 360, 100, 100)
        direction_image.composite_draw(0, 'h', 50, 360, 100, 100)

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
                selected_class = map_list[selection_index]
                select_character.set_background(selected_class)
                play_mode.set_background_class(selected_class)
                game_framework.change_mode(select_character)