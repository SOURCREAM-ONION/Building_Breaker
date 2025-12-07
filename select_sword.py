from pico2d import *
import game_framework
import select_map
import select_character
import play_mode
from sword import Sword, WoodenSword, AncientSword, BloodSword, CheckinSword, CutterSword, GreenSword, IceSword, LibertySword, LightningSword, GoldenSword, NeptuneSword, NightSword, PinkSword, RosenSword, SharkSword, SyringeSword, BlackpinkSword
import game_data

direction_image = None
background = None
character = None
current_sword = None

current_map_class = None
current_character_class = None

def set_background_class(cls):
    global current_map_class
    current_map_class = cls

def set_character_class(cls):
    global current_character_class
    current_character_class = cls

def init():
    global sword_list, selection_index, current_sword
    global direction_image, background, character

    sword_list = [Sword, WoodenSword, AncientSword, BloodSword, CheckinSword, CutterSword, GreenSword, IceSword, LibertySword, LightningSword, GoldenSword, NeptuneSword, NightSword, PinkSword, RosenSword, SharkSword, SyringeSword, BlackpinkSword]
    selection_index = 0

    if current_map_class:
        background = current_map_class()

    if current_character_class:
        character = current_character_class()

    if character:
        current_sword = sword_list[selection_index](character)

    direction_image = load_image("ui/Direction_21.png")

def finish():
    global current_sword, direction_image, background, character

    if current_sword: del current_sword
    if direction_image: del direction_image
    if background: del background
    if character: del character

def update():
    pass

def draw():
    clear_canvas()

    if background:
        background.draw()

    if character:
        character.draw()

    if current_sword:
        current_sword.draw()

    if direction_image:
        direction_image.draw(430, 160, 100, 100)
        direction_image.composite_draw(0, 'h', 50, 160, 100, 100)

    update_canvas()

def handle_events():
    global selection_index, current_sword, character

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(select_character)
            elif event.key == SDLK_LEFT: # 왼쪽 화살표 키 입력
                selection_index = (selection_index - 1) % len(sword_list)
                del current_sword
                current_sword = sword_list[selection_index](character)
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if character: character.draw()
                if current_sword: current_sword.draw()
                direction_image.composite_draw(0, 'h', 60, 160, 120, 120)
                direction_image.draw(430, 160, 100, 100)
                update_canvas()
                delay(0.1)  # 0.1초 대기
            elif event.key == SDLK_RIGHT: # 오른쪽 화살표 키 입력
                selection_index = (selection_index + 1) % len(sword_list)
                del current_sword
                current_sword = sword_list[selection_index](character)
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if character: character.draw()
                if current_sword: current_sword.draw()
                direction_image.draw(420, 160, 120, 120)
                direction_image.composite_draw(0, 'h', 50, 160, 100, 100)
                update_canvas()
                delay(0.1)  # 0.1초 대기
            elif event.key == SDLK_SPACE:
                selected_sword_class = sword_list[selection_index]

                # play_mode에 무기 설정
                play_mode.set_sword_class(selected_sword_class)

                game_framework.change_mode(play_mode)