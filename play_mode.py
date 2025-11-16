from pico2d import *
import game_world
from character import Character
from sword import Sword
import game_framework
import title_mode
from building import Building



def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_KEYDOWN:
            character.handle_event(event)
            sword.state_machine.handle_event(('INPUT', event))

def init(): # 월드가 새로 나올때 그려지는 부분
    global running
    global character
    global world
    global sword
    global building

    running = True
    world = []
    game_world.clear()

    sword = Sword()
    game_world.add_object(sword, 2)

    character = Character()
    game_world.add_object(character, 0)

    building = Building()
    game_world.add_object(building, 1)


def update(): # 월드에 객체가 추가되는 부분
    game_world.update()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if bottom_a > top_b: return False
    return True

def draw(): # 월드가 만들어지는 부분
    clear_canvas()
    game_world.render()
    update_canvas()

def finish(): # 월드가 사라질때 지워지는 부분
    pass