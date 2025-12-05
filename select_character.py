from pico2d import *
import game_framework
import play_mode
import title_mode
import select_map
from character import Character, Char2

direction_image = None

def init():
    global character_list
    global selection_index
    global current_character
    global direction_image

    character_list = [Character, Char2]
    selection_index = 0

    current_character = character_list[selection_index]()

    direction_image = load_image("Direction_21.png")

def finish():
    global current_character
    global direction_image

    del current_character
    del direction_image

def update():
    pass

def draw():
    clear_canvas()

    current_character.draw()
    if direction_image:
        direction_image.draw(430, 360, 100, 100)
        direction_image.composite_draw(0, 'h', 50, 360, 100, 100)

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
            elif event.key == SDLK_LEFT: # 왼쪽 화살표 키 입력
                selection_index = (selection_index - 1) % len(character_list)
                del current_character
                current_character = character_list[selection_index]()
            elif event.key == SDLK_RIGHT: # 오른쪽 화살표 키 입력
                selection_index = (selection_index + 1) % len(character_list)
                del current_character
                current_character = character_list[selection_index]()
            elif event.key == SDLK_SPACE:
                play_mode.character_class = character_list[selection_index]
                game_framework.change_mode(play_mode)