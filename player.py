from pico2d import *

open_canvas()



class Character:
    def __init__(self, image):
        self.image = load_image('char1_1.png')
    def draw(self):
        self.image.draw(400, 30)
    def update(self):
        pass

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