from pico2d import *

open_canvas()



class Character:
    def __init__(self, image):
        self.image = load_image('char1_1.png')
        self.frame = 0
        self.x, self.y = 400, 30
    def draw(self):
        self.frame = (self.frame + 1) % 3
    def update(self):
        self.image.clip_draw(self.frame * 30, 30, 30, 30, 400, 300, 50, 50)

def reset_world():
    global running
    global character

    running = True
    character = Character()


def update_world():
    character.update()

def render_world():
    clear_canvas()
    character.draw()
    update_canvas()

close_canvas()