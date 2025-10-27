from pico2d import *

open_canvas()

character = load_image('char1_1.png')
sword = load_image('basic_sword.png')

framec = 0;
frames = 0
while True:
    clear_canvas()
    character.clip_draw(framec * 30, 30, 30, 30, 400, 300, 50, 50)
    framec = (framec + 1) % 3
    sword.clip_draw(frames * 203, 0, 203, 350, 410, 310, 50, 50)
    frames = (frames + 1) % 10
    update_canvas()
    delay(0.3)


close_canvas()