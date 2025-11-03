from pico2d import *

open_canvas()

running = True

class Character:
    def __init__(self, image):
        self.image = load_image('char1_1.png')
        self.frame = 0
        self.x, self.y = 400, 30
    def draw(self):
        self.frame = (self.frame + 1) % 3
    def update(self):
        self.image.clip_draw(self.frame * 30, 30, 30, 30, 400, 300, 50, 50)

while running:
    update_world()
    render_world()
    delay(0.1)

close_canvas()