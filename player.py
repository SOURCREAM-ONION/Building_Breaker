from pico2d import *





class Character:
    def __init__(self):
        self.image = load_image('char1_1.png')
        self.frame = 0
        self.x, self.y = 400, 30
    def draw(self):
        self.frame = (self.frame + 1) % 3
    def update(self):
        self.image.clip_draw(self.frame * 30, 30, 30, 30, 400, 300, 50, 50)

open_canvas()

def reset_world():
    global running
    global character

    running = True
    world = []
    character = Character()
    world.append(character)

reset_world()

def update_world():
    character.update()


def render_world():
    clear_canvas()
    character.draw()
    update_canvas()


while running:
    update_world()
    render_world()
    delay(0.1)

close_canvas()