from pico2d import *
import game_framework
import play_mode
import select_map
from character import Character,Char12, Char13, Char21, Char22, Char23, Char31, Char32, Char33, Char41, Char42, Char43, Char51, Char52, Char53
import select_sword
import game_data

direction_image = None
background = None
current_character = None

current_map_class = None

def set_background(cls):
    global current_map_class
    if current_map_class:
        del current_map_class
    current_map_class = cls

def init():
    global character_list
    global selection_index
    global current_character
    global direction_image
    global background

    character_list = [Character, Char12, Char13, Char21, Char22, Char23, Char31, Char32, Char33, Char41, Char42, Char43, Char51, Char52, Char53]
    selection_index = 0

    if current_map_class:
        background = current_map_class()

    current_character = character_list[selection_index]()

    direction_image = load_image("ui/Direction_21.png")

def finish():
    global current_character
    global direction_image
    global background

    del current_character
    del direction_image
    if background:
        del background
        background = None

def update():
    pass

def draw():
    clear_canvas()

    if background:
        background.draw()

    if current_character:
        current_character.draw()

    if direction_image:
        direction_image.draw(430, 160, 100, 100)
        direction_image.composite_draw(0, 'h', 50, 160, 100, 100)

    update_canvas()

def handle_events():
    global selection_index, current_character

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(select_map) # esc 누르면 맵 선택으로 감
            elif event.key == SDLK_LEFT:
                selection_index = (selection_index - 1) % len(character_list)
                del current_character
                current_character = character_list[selection_index]()
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if current_character: current_character.draw()
                direction_image.composite_draw(0, 'h', 60, 160, 120, 120)
                direction_image.draw(430, 160, 100, 100)
                update_canvas()
                delay(0.1)
            elif event.key == SDLK_RIGHT:
                selection_index = (selection_index + 1) % len(character_list)
                del current_character
                current_character = character_list[selection_index]()
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if current_character: current_character.draw()
                direction_image.draw(420, 160, 120, 120)
                direction_image.composite_draw(0, 'h', 50, 160, 100, 100)
                update_canvas()
                delay(0.1)
            elif event.key == SDLK_SPACE:
                selected_character_class = character_list[selection_index]
                play_mode.set_character_class(selected_character_class)
                select_sword.set_background_class(current_map_class)
                select_sword.set_character_class(selected_character_class)
                game_framework.change_mode(select_sword)