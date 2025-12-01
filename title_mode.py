from pico2d import *
import game_framework
import play_mode

image = None
font = None

def init():
    global image, font
    image = load_image('title.png')
    font = load_font('ENCR10B.ttf', 25)

def finish():
    global image, font
    del image
    del font

def update():
    pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw_to_origin(0,0, 400, 600)
    font.draw(50, 80, 'Press SPACE to Start', (0, 37, 135))
    font.draw(50, 80, 'Press SPACE to Start', (0, 37, 135))
    font.draw(50, 80, 'Press SPACE to Start', (0, 37, 135))
    update_canvas()