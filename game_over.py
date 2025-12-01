from pico2d import *
import game_framework
import play_mode
import title_mode

image = None

def init():
    global image
    image = load_image('EndBackground.png')

def finish():
    global image
    del image

def update():
    pass

def handle_events():
    pass

def draw():
    pass