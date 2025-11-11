from pico2d import *

import game_world
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
            sword.state_machine.handle_event(('INPUT', event))

open_canvas()

def reset_world(): # 월드가 새로 나올때 그려지는 부분
    global running
    global character
    global world
    global sword

    running = True
    world = []

    sword = Sword()
    game_world.add_object(sword, 2)

    character = Character()
    game_world.add_object(character, 0)

reset_world()

def update_world(): # 월드에 객체가 추가되는 부분
    game_world.update()


def render_world(): # 월드가 만들어지는 부분
    clear_canvas()
    game_world.render()
    update_canvas()





while running:
    handle_events()
    update_world()
    render_world()
    delay(0.07)

close_canvas()