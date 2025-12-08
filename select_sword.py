from pico2d import *
import game_framework
import select_character
import play_mode
from sword import Sword, WoodenSword, AncientSword, BloodSword, CheckinSword, CutterSword, GreenSword, IceSword, LibertySword, LightningSword, GoldenSword, NeptuneSword, NightSword, PinkSword, RosenSword, SharkSword, SyringeSword, BlackpinkSword
from coin import CoinBox
import game_data

direction_image = None
background = None
character = None
current_sword = None

current_map_class = None
current_character_class = None
sword_prices = [] # 검 가격 리스트

# 알림
notification_msg = None
notification_timer = 0.0 # 알림 타이머

def set_background_class(cls):
    global current_map_class
    current_map_class = cls

def set_character_class(cls):
    global current_character_class
    current_character_class = cls

def init():
    global sword_list, selection_index, current_sword
    global direction_image, background, character, sword_prices, coin_box, font_unlock, font_notification, notification_msg, notification_timer # 상점 관련 전역 변수

    sword_list = [Sword, WoodenSword, AncientSword, BloodSword, CheckinSword, CutterSword, GreenSword, IceSword, LibertySword, LightningSword, GoldenSword, NeptuneSword, NightSword, PinkSword, RosenSword, SharkSword, SyringeSword, BlackpinkSword]
    selection_index = 0

    sword_prices = [0, 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9, 10, 15, 20, 25]  # 각 검의 가격 설정

    for price in sword_prices:
        if price == 0:
            game_data.unlocked_swords.append(True)
        else:
            game_data.unlocked_swords.append(False)

    notification_msg = None
    notification_timer = 0.0

    if current_map_class:
        background = current_map_class() # 선택한 배경 보이게 하기

    if current_character_class:
        character = current_character_class() # 선택한 캐릭터 보이게 하기

    if character:
        current_sword = sword_list[selection_index](character)

    direction_image = load_image("ui/Direction_21.png")
    coin_box = CoinBox()

    font_unlock = load_font("ui/ENCR10B.TTF", 40)
    font_notification = load_font("ui/ENCR10B.TTF", 20)

def finish():
    global current_sword, direction_image, background, character
    global font_unlock, font_notification, notification_msg, notification_timer

    if current_sword: del current_sword
    if direction_image: del direction_image
    if background: del background
    if character: del character
    del font_unlock
    del font_notification

def update():
    pass

def draw():
    clear_canvas()

    if background:
        background.draw()

    if character:
        character.draw()

    if current_sword:
        current_sword.draw()

    if direction_image:
        direction_image.draw(430, 160, 100, 100)
        direction_image.composite_draw(0, 'h', 50, 160, 100, 100)

    if coin_box:
        coin_box.draw()

    is_unlocked = game_data.unlocked_swords[selection_index]

    if not is_unlocked:
        font_unlock.draw(160, 600, "LOCKED", (255, 0, 0))
        font_unlock.draw(120, 550, f"Price: {sword_prices[selection_index]}", (255, 255, 255))
        # 구매 안내 문구 추가
        font_unlock.draw(70, 200, "[Space] to Buy", (200, 200, 200))

    update_canvas()

def handle_events():
    global selection_index, current_sword, character, notification_msg, notification_timer

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(select_character)
            elif event.key == SDLK_LEFT: # 왼쪽 화살표 키 입력
                selection_index = (selection_index - 1) % len(sword_list)
                del current_sword
                current_sword = sword_list[selection_index](character)
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if character: character.draw()
                if current_sword: current_sword.draw()
                direction_image.composite_draw(0, 'h', 60, 160, 120, 120)
                direction_image.draw(430, 160, 100, 100)
                coin_box.draw()
                update_canvas()
                delay(0.1)  # 0.1초 대기
            elif event.key == SDLK_RIGHT: # 오른쪽 화살표 키 입력
                selection_index = (selection_index + 1) % len(sword_list)
                del current_sword
                current_sword = sword_list[selection_index](character)
                # 확대 이미지 그리기
                clear_canvas()
                if background: background.draw()
                if character: character.draw()
                if current_sword: current_sword.draw()
                direction_image.draw(420, 160, 120, 120)
                direction_image.composite_draw(0, 'h', 50, 160, 100, 100)
                coin_box.draw()
                update_canvas()
                delay(0.1)  # 0.1초 대기
            elif event.key == SDLK_SPACE:
                if game_data.unlocked_swords[selection_index]:
                    selected_sword_class = sword_list[selection_index]
                    play_mode.set_sword_class(selected_sword_class)
                    game_framework.change_mode(play_mode)
                else:
                    # 잠겨있으면 구매 시도
                    price = sword_prices[selection_index]

                    if game_data.total_coins >= price:
                        game_data.total_coins -= price
                        game_data.unlocked_swords[selection_index] = True  # game_data에 저장

                        notification_msg = f"Map {selection_index} Unlocked!"
                        notification_timer = get_time() + 1.0
                    else:
                        notification_msg = "Not enough coins!"
                        notification_timer = get_time() + 1.0