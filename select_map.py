from pico2d import *
import game_framework
import play_mode
from background import Background2, Background3

def init():
    global map_list
    global selection_index
    global current_preview

    map_list = [Background2, Background3]
    selection_index = 0

    current_preview = map_list[selection_index]()

def finish():
    global current_preview
    del current_preview

def update():
    pass

def draw():
    clear_canvas()

    current_preview.draw()

    pass

    update_canvas()

def handle_events():
    global selection_index, current_preview

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(play_mode)
            elif event.key == SDLK_LEFT: # 왼쪽 화살표 키 입력
                selection_index = (selection_index - 1) % len(map_list)
                del current_preview
                current_preview = map_list[selection_index]()
            elif event.key == SDLK_RIGHT: # 오른쪽 화살표 키 입력
                selection_index = (selection_index + 1) % len(map_list)
                del current_preview
                current_preview = map_list[selection_index]()
            elif event.key == SDLK_SPACE:
                # 선택된 맵으로 플레이 모드 전환
                selected_class = map_list[selection_index]

                # 이 줄이 꼭 있어야 play_mode의 변수가 바뀝니다.
                play_mode.set_background_class(selected_class)
                game_framework.change_mode(play_mode)