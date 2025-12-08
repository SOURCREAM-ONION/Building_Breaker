from pico2d import *
import game_framework
import play_mode
import select_map
from character import Character,Char12, Char13, Char21, Char22, Char23, Char31, Char32, Char33, Char41, Char42, Char43, Char51, Char52, Char53
import select_sword
from coin import CoinBox
import game_data

direction_image = None
background = None
current_character = None

current_map_class = None
character_prices = [] # 캐릭터 가격 리스트

# 알림
notification_msg = None
notification_timer = 0.0 # 알림 타이머

def set_background(cls):
    global current_map_class
    if current_map_class:
        del current_map_class
    current_map_class = cls

def init():
    global character_list, selection_index
    global current_character, direction_image, background, coin_box, character_prices, font_unlock, font_notification, notification_msg,notification_timer # 상점 관련 전역 변수

    coin_box = CoinBox()

    character_list = [Character, Char12, Char13, Char21, Char22, Char23, Char31, Char32, Char33, Char41, Char42, Char43, Char51, Char52, Char53]

    selection_index = 0
    character_prices = [0,1,1,1,2,2,2,3,3,4,4,5,5,6,7]  # 각 캐릭터의 가격 설정

    for price in character_prices:
        if price == 0:
            game_data.unlocked_characters.append(True)
        else:
            game_data.unlocked_characters.append(False)

    notification_msg = None
    notification_timer = 0.0

    if current_map_class:
        background = current_map_class()

    current_character = character_list[selection_index]()

    direction_image = load_image("ui/Direction_21.png")
    font_unlock = load_font("ui/ENCR10B.TTF", 40)
    font_notification = load_font("ui/ENCR10B.TTF", 20)

def finish():
    global current_character
    global direction_image
    global background
    global font_unlock, font_notification

    del current_character
    del direction_image
    if background:
        del background
        background = None
    del font_unlock
    del font_notification

def update():
    pass

def draw():
    clear_canvas()

    if background:
        background.draw()

    if current_character:
        current_character.draw()

    if coin_box:
        coin_box.draw()

    if direction_image:
        direction_image.draw(430, 160, 100, 100)
        direction_image.composite_draw(0, 'h', 50, 160, 100, 100)

    is_unlocked = game_data.unlocked_characters[selection_index]

    if not is_unlocked:
        font_unlock.draw(160, 600, "LOCKED", (255, 0, 0))
        font_unlock.draw(120, 550, f"Price: {character_prices[selection_index]}", (255, 255, 255))
        # 구매 안내 문구 추가
        font_unlock.draw(70, 200, "[Space] to Buy", (200, 200, 200))

    # 알림 메시지 출력
    if notification_msg and get_time() < notification_timer:
        font_notification.draw(130, 400, notification_msg, (255, 255, 0))


    update_canvas()

def handle_events():
    global selection_index, current_character, notification_msg, notification_timer

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(select_map) # esc 누르면 맵 선택으로 감
            elif event.key == SDLK_LEFT:
                selection_index = (selection_index - 1) % len(character_list)
                del current_character
                current_character = character_list[selection_index]()
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if current_character: current_character.draw()
                direction_image.composite_draw(0, 'h', 60, 160, 120, 120)
                direction_image.draw(430, 160, 100, 100)
                coin_box.draw()
                update_canvas()
                delay(0.1)
            elif event.key == SDLK_RIGHT:
                selection_index = (selection_index + 1) % len(character_list)
                del current_character
                current_character = character_list[selection_index]()
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if current_character: current_character.draw()
                direction_image.draw(420, 160, 120, 120)
                direction_image.composite_draw(0, 'h', 50, 160, 100, 100)
                coin_box.draw()
                update_canvas()
                delay(0.1)
            elif event.key == SDLK_SPACE:
                if game_data.unlocked_characters[selection_index]:
                    selected_character_class = character_list[selection_index]
                    play_mode.set_character_class(selected_character_class)
                    select_sword.set_background_class(current_map_class)
                    select_sword.set_character_class(selected_character_class)
                    game_framework.change_mode(select_sword)
                else:
                    # 잠겨있으면 구매 시도
                    price = character_prices[selection_index]

                    if game_data.total_coins >= price:
                        game_data.total_coins -= price
                        game_data.unlocked_characters[selection_index] = True  # game_data에 저장

                        notification_msg = f"Map {selection_index} Unlocked!"
                        notification_timer = get_time() + 1.0
                    else:
                        notification_msg = "Not enough coins!"
                        notification_timer = get_time() + 1.0