from pico2d import *

from character import Character
from sword import Sword


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_KEYDOWN:
            character.handle_event(event)

open_canvas()

def reset_world(): # 월드가 새로 나올때 그려지는 부분
    global running
    global character
    global world
    global sword

    running = True
    world = []

    sword = Sword()
    world.append(sword)

    character = Character()
    world.append(character)

reset_world()

def update_world(): # 월드에 객체가 추가되는 부분
    for game_object in world:
        game_object.update()


def render_world(): # 월드가 만들어지는 부분
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()





while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)

close_canvas()