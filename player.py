from pico2d import *

class Character:
    def __init__(self): # 캐릭터가 처음 생성될 때 나오는 부분
        self.x, self.y = 400, 300
        self.frame = 0
        self.image = load_image('Char1_1.png')

    def draw(self):  # 캐릭터가 그려지는 부분
        self.frame = (self.frame + 1) % 3

    def update(self): # 캐릭터가 업데이트 되는 부분
        self.image.clip_draw(self.frame * 30, 30, 30, 30, 400, 300)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas()

def reset_world(): # 월드가 새로 나올때 그려지는 부분
    global running
    global character
    global world

    running = True
    world = []
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
    delay(0.05)

close_canvas()