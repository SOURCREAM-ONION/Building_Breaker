from pico2d import *
import game_world
from character import Character
import game_framework
import title_mode
from building import create_random_building,Building
from background import Background # 배경 클래스 임포트
from sword import Sword
from coin import Coin

current_map_class = Background  # 현재 맵 클래스를 Background로 설정
current_character_class = Character # 현재 캐릭터 클래스를 Character로 설정
current_sword_class = Sword # 현재 검 클래스를 Sword로 설정

def set_background_class(cls):
    global current_map_class
    current_map_class = cls

def set_character_class(scc):
    global current_character_class
    current_character_class = scc

def set_sword_class(scs):
    global current_sword_class
    current_sword_class = scs

# 충돌 체크 함수 추가
def collide_bb(bb_a, bb_b):
    if bb_a is None or bb_b is None:  # None 체크 추가
        return False

    left_a, bottom_a, right_a, top_a = bb_a
    left_b, bottom_b, right_b, top_b = bb_b

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_KEYDOWN:
            character.handle_event(event)
            sword.handle_event(event)

score = 0
score_timer = 0.0
coin_spawn_timer = 0.0
font = None

def init():  # 월드가 새로 나올때 그려지는 부분
    global running, character, world, sword, building, spawn_timer, coin
    global score, score_timer, font # 점수와 타이머, 폰트 전역 변수 선언

    running = True
    world = [[],[],[]]
    game_world.clear()

    background = current_map_class()
    game_world.add_object(background, 0) # 배경을 월드의 0번 레이어에 추가

    character = current_character_class() # 캐릭터 객체 생성
    game_world.add_object(character, 1) # 캐릭터를 월드의 1번 레이어에 추가

    sword = current_sword_class(character) # 검 객체 생성
    game_world.add_object(sword, 1) # 검을 월드의 0번 레이어에 추가

    building = create_random_building() # 빌딩 객체 생성
    game_world.add_object(building, 1) # 빌딩을 월드의 0번 레이어에 추가

    coin = Coin()
    game_world.add_object(coin, 1)

    spawn_timer = 0.0

    # 점수 및 폰트 초기화
    score = 0
    score_timer = 0.0
    font = load_font('ui/ENCR10B.ttf', 30)


def update():  # 월드에 객체가 추가되는 부분
    global spawn_timer, score, score_timer, coin_spawn_timer
    game_world.update()

    # 점수 업데이트
    score_timer += game_framework.frame_time
    if score_timer >= 1.0:  # 1초마다 점수 증가
        score += 1  # 점수 10점 증가
        score_timer -= 0.0  # 타이머 초기화

    coin_spawn_timer += game_framework.frame_time
    if coin_spawn_timer >= 3.0:
        new_coin = Coin()
        game_world.add_object(new_coin, 1)
        coin_spawn_timer = 0.0

    # 건물이 일정 위치에 도달하면 게임오버
    for obj in game_world.world[1]: # for문으로 월드의 0번 레이어 객체들 검사
        if isinstance(obj, Building): # 만약 Building 객체라면
            for i in range(obj.num_floors): # 각 층을 검사
                if obj.floors[i]['alive']: # 층이 살아있다면
                    floor_y = obj.y + obj.floors[i]['y_offset'] # 층의 현재 y 위치 계산
                     # 층의 바닥이 y=20 이하로 내려갔는지 확인
                    if floor_y <= 150:
                        import game_over
                        game_framework.change_mode(game_over)
                        return

    # # 빌딩 스폰 타이머 업데이트
    # spawn_timer += game_framework.frame_time
    # if spawn_timer >= 15.0:
    #     spawn_timer = 0.0
    #     new_building = create_random_building()
    #     game_world.add_object(new_building, 0)

    # 완전히 파괴한 빌딩 제거
    for obj  in list(game_world.world[1]): # for문으로 월드의 0번 레이어 객체들 검사
        if isinstance(obj, Building): # 만약 Building 객체라면
            all_destroyed = True # 모든 층이 파괴되었는지 확인하는 변수
            for floor in obj.floors: # 각 층을 검사
                if floor['alive']: # 층이 하나라도 살아있다면
                    all_destroyed = False # all_destroyed를 False로
                    break

            if all_destroyed: # 모든 층이 파괴되었다면
                game_world.remove_object(obj) # 빌딩 제거

    # 빌딩이 하나도 없으면 새 빌딩 생성
    building_exists = False
    for obj in game_world.world[1]: # for문으로 월드의 0번 레이어 객체들 검사
        if isinstance(obj, Building): # 만약 Building 객체라면
            building_exists = True # 빌딩이 존재함
            break

    if not building_exists: # 빌딩이 없으면
        new_building = create_random_building() # 새 빌딩 생성
        game_world.add_object(new_building, 1) # 월드에 추가
        print("새 빌딩 생성됨") # 디버그 메시지

    # 검 공격 중일 때 모든 빌딩과 충돌 체크
    if sword.is_attacking(): # 검을 휘두르는 중이라면
        for obj in game_world.world[1]: # for문으로 월드의 1번 레이어 객체들 검사
            if isinstance(obj, Building): # 만약 Building 객체라면
                for i in range(obj.num_floors): # 각 층을 검사
                    bb = obj.get_bb_floor(i) # 층의 충돌 박스 가져오기
                    if bb and collide_bb(bb, sword.get_bb()): # 충돌 박스가 존재하고 충돌했다면
                        if (obj, i) not in sword.hit_list: # 이미 히트리스트에 없다면
                            obj.take_damage(i,1) # 해당 층에 데미지 1 입히기
                            sword.hit_list.append((obj, i)) # 히트리스트에 추가

                            if not obj.floors[i]['alive']: # 만약 해당 층이 파괴되었다면
                                score += 10  # 점수 100점 추가

    # 검 방어 중일 때 모든 빌딩과 충돌 체크
    if sword.is_defending(): # 검으로 방어하는 중이라면
        for obj in game_world.world[1]: # for문으로 월드의 1번 레이어 객체들 검사
            if isinstance(obj, Building): # 만약 Building 객체라면
                for i in range(obj.num_floors): # 각 층을 검사
                    bb = obj.get_bb_floor(i) # 층의 충돌 박스 가져오기
                    if bb and collide_bb(bb, sword.get_aa()): # 충돌 박스가 존재하고 충돌했다면
                        obj.push_up() # 빌딩 튕겨 올리기
                        character.velocity_y = -800 # 캐릭터를 강제로 아래로 떨어뜨림

    character_bb = character.get_bb()  # 캐릭터의 현재 충돌 박스

    # 빌딩과 캐릭터의 충돌 체크
    for obj in game_world.world[1]: # for문으로 월드의 1번 레이어 객체들 검사
        if isinstance(obj, Building):  # 빌딩 객체 찾기
            for i in range(obj.num_floors): # 각 층을 검사
                floor_bb = obj.get_bb_floor(i) # 층의 충돌 박스 가져오기
                if floor_bb and collide_bb(character_bb, floor_bb):# 건물의 층과 캐릭터가 충돌했다면
                    character.y = floor_bb[1] - 50 # 캐릭터를 층 위에 위치시킴
                    if character.velocity_y > 0: # 캐릭터가 점프 중(위로 올라가는 중)이라면
                        character.velocity_y = 0  # 상승력을 없애 바로 떨어지게 함

    # 코인과 캐릭터의 충돌 체크
    for obj in list(game_world.world[1]): # for문으로 월드의 1번 레이어 객체들 검사
        if isinstance(obj, Coin):  # 코인 객체 찾기
            coin_bb = obj.get_bb() # 코인의 충돌 박스 가져오기
            if coin_bb and collide_bb(character_bb, coin_bb):# 코인과 캐릭터가 충돌했다면
                game_world.remove_object(obj) # 코인 제거


def draw():  # 월드가 만들어지는 부분
    clear_canvas()
    game_world.render()

    # 점수 표시
    if font:
        font.draw(20, 680, f'Score : {score}',(255,255,255))
    update_canvas()


def finish():  # 월드가 사라질때 지워지는 부분
    global font
    if font:
        del font