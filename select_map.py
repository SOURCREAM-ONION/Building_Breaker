from pico2d import *
import game_framework
import play_mode
import title_mode
import select_character
from background import Background2, Background3, Background4, Background5

direction_image = None

def init():
    global map_list
    global selection_index
    global current_preview
    global direction_image

    map_list = [Background2, Background3, Background4, Background5]
    selection_index = 0

    current_preview = map_list[selection_index]()

    direction_image = load_image("Direction_21.png")

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
                del current_preview
                current_preview = map_list[selection_index]()
            elif event.key == SDLK_RIGHT: # 오른쪽 화살표 키 입력
                selection_index = (selection_index + 1) % len(map_list)
                del current_preview
                current_preview = map_list[selection_index]()
            elif event.key == SDLK_SPACE:
                selected_class = map_list[selection_index]
                play_mode.set_background_class(selected_class)
                game_framework.change_mode(select_character)