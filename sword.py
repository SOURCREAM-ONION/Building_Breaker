from pico2d import *
from state_machine import StateMachine
from character import Character, mouse_left_click, time_out, mouse_right_click, jump_key_press

import game_framework

# 검 대기 상태
class Idle_Sword:
    def __init__(self, sword):
        self.sword = sword
        self.frame = 0 # 검 대기 애니메이션 프레임 초기화

    def enter(self):
        self.frame = 0

    def exit(self):
        pass

    def do(self):
        self.sword.x = self.sword.character.x + 44
        self.sword.y = self.sword.character.y

    def draw(self):
        import math
        import play_mode
        screen_y = self.sword.y - play_mode.camera_y
        self.sword.image.clip_composite_draw(0, 0, 122, 122, -math.pi / 2, '', self.sword.x, screen_y, 200, 200)


# 검 휘두르기 상태
class Wield_Sword:
    images = None

    def __init__(self, sword):
        self.x, self.y = 200, 53
        self.sword = sword
        self.frame = 0
        self.frame_count = 6
        self.TIME_PER_ACTION = 1.0 / 0.09 # 검 휘두르기 애니메이션 속도
        self.ACTION_PER_TIME = 1.0 / 0.09 # 검 휘두르기 애니메이션 동작 시간
        self.FRAMES_PER_ACTION = 6 # 검 휘두르기 애니메이션 프레임 수
        self.framex = 240
        self.framey = 200

    def enter(self):
        self.frame = 0
        self.sword.hit_list.clear() # 검이 공격한 대상 리스트 초기화

    def exit(self):
        pass

    def do(self):
        self.frame = self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time # 프레임을 시간처리
        if self.frame >= self.frame_count:
            self.sword.state_machine.handle_event(('TIME_OUT', None))

        self.sword.x = self.sword.character.x
        self.sword.y = self.sword.character.y + 46

    def draw(self):
        import play_mode
        screen_y = self.sword.y - play_mode.camera_y
        frame_index = int(self.frame)
        # clip_draw의 y좌표 인자에 screen_y 사용
        # (예시)
        if frame_index == 0:
            self.sword.image.clip_draw(0, 0, 204, 122, self.sword.x, screen_y, self.framex, self.framey)
        elif frame_index == 1:
            self.sword.image.clip_draw(204, 0, 204, 122, self.sword.x, screen_y, self.framex, self.framey)
        elif frame_index == 2:
            self.sword.image.clip_draw(408, 0, 204, 122, self.sword.x, screen_y, self.framex, self.framey)
        elif frame_index == 3:
            self.sword.image.clip_draw(612, 0, 204, 122, self.sword.x, screen_y, self.framex, self.framey)
        elif frame_index == 4:
            self.sword.image.clip_draw(816, 0, 204, 122, self.sword.x, screen_y, self.framex, self.framey)
        elif frame_index == 5:
            self.sword.image.clip_draw(1020, 0, 204, 122, self.sword.x, screen_y, self.framex, self.framey)


# 검 방어 상태
class Defence_Sword:
    def __init__(self, sword):
        self.sword = sword
        self.frame = 0 # 검 방어 애니메이션 프레임 초기화
        self.frame_count = 1 # 검 방어 애니메이션 프레임 수
        self.TIME_PER_ACTION = 5 # 검 방어 애니메이션 속도
        self.ACTION_PER_TIME = 2.7 # 검 방어 애니메이션 동작 시간
        self.FRAMES_PER_ACTION = 1 # 검 방어 애니메이션 프레임 수

    def enter(self):
        self.frame = 0
        self.sword.x = self.sword.character.x - 80
        self.sword.y = self.sword.character.y - 55

    def exit(self):
        pass

    def do(self):
        self.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.frame >= self.frame_count:
            self.sword.state_machine.handle_event(('TIME_OUT', None))


        self.sword.x = self.sword.character.x - 80
        self.sword.y = self.sword.character.y - 55


    def draw(self):
        import math
        import play_mode
        screen_y = self.sword.y - play_mode.camera_y
        self.sword.image.clip_composite_draw(0, 0, 204, 122, math.pi, '', self.sword.x, screen_y, 300, 200)


# 검 클래스 정의
class Sword:
    def __init__(self, character):
        self.character = character
        self.x, self.y = character.x + 22, character.y # 초기 위치 설정 # 검의 초기 위치
        self.image = load_image('sword/basic_sword.png') # 검의 이미지 로드
        self.last_defence_time = 0.0 # 마지막 방어 시간 초기화
        self.defence_cooltime = 2.0
        self.damage = 1
        self.hit_list = []

        self.hit_list = []  # 검이 공격한 대상 리스트 초기화

        self.IDLE_SWORD = Idle_Sword(self)
        self.WIELD_SWORD = Wield_Sword(self)
        self.DEFENCE_SWORD = Defence_Sword(self)
        self.state_machine = StateMachine(
            self.IDLE_SWORD,
                    {
                        self.IDLE_SWORD: {mouse_left_click: self.WIELD_SWORD, mouse_right_click: self.DEFENCE_SWORD}, # IDLE상태일 때 일어나는 이벤트
                        self.WIELD_SWORD: {time_out : self.IDLE_SWORD}, # WIELD상태일 때 일어나는 이벤트
                        self.DEFENCE_SWORD: {time_out : self.IDLE_SWORD} # DEFENCE상태일 때 일어나는 이벤트
                    }
        )


    # 방어 쿨타임 체크 함수
    def can_defence(self):
        import time
        current_time = time.time()
        if current_time - self.last_defence_time >= self.defence_cooltime:
            self.last_defence_time = current_time
            return True
        return False

    def update(self):
        self.state_machine.update()

    def draw(self):
        import play_mode
        self.state_machine.draw()
        # cy = play_mode.camera_y
        #
        # if self.state_machine.current_state == self.WIELD_SWORD:
        #     l, b, r, t = self.get_bb()
        #     draw_rectangle(l, b - cy, r, t - cy)
        # elif self.state_machine.current_state == self.DEFENCE_SWORD:
        #     l, b, r, t = self.get_aa()
        #     draw_rectangle(l, b - cy, r, t - cy)

    # 검의 방어 충돌박스
    def get_aa(self):
        return self.x - 0, self.y + 60, self.x + 160, self.y + 100

    # 검의 공격 충돌박스
    def get_bb(self):
        return self.x - 80, self.y - 40, self.x + 80, self.y + 80

    # 검이 공격 중인지 확인
    def is_attacking(self):
        return self.state_machine.current_state == self.WIELD_SWORD

    # 검이 방어 중인지 확인
    def is_defending(self):
        return self.state_machine.current_state == self.DEFENCE_SWORD

    def handle_event(self, event):
        # 방어 입력 시 쿨다운 체크
        if mouse_right_click(('INPUT', event)):
            if self.can_defence():
                self.state_machine.handle_event(('INPUT', event))
        else:
            self.state_machine.handle_event(('INPUT', event))

class WoodenSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/wooden_sword.png')  # 나무 검 이미지 로드
        self.damage = 1

class AncientSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/ancient_sword.png')  # 고대 검 이미지 로드
        self.damage = 2

class BloodSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/blood_sword.png')  # 피의 검 이미지 로드
        self.damage = 3

class CheckinSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/checkin_sword.png')  # 체크인 검 이미지 로드
        self.damage = 4

class CutterSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/cutter_sword.png')  # 커터 검 이미지 로드
        self.damage = 4

class GreenSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/greed_sword.png')  # 그린 검 이미지 로드
        self.damage = 5

class IceSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/ice_sword.png')  # 아이스 검 이미지 로드
        self.damage = 5

class LibertySword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/liberty_sword.png')  # 리버티 검 이미지 로드
        self.damage = 6

class LightningSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/lightning_sword.png')  # 라이트닝 검 이미지 로드
        self.damage = 6

class GoldenSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/golden_sword.png')  # 골든 검 이미지 로드
        self.damage = 6

class NeptuneSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/neptune_sword.png')  # 넵튠 검 이미지 로드
        self.damage = 7

class NightSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/night_sword.png')  # 나이트 검 이미지 로드
        self.damage = 7

class PinkSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/pink_sword.png')  # 핑크 검 이미지 로드
        self.damage = 7

class RosenSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/rosen_sword.png')  # 로젠 검 이미지 로드
        self.damage = 7

class SharkSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/shark_sword.png')  # 샤크 검 이미지 로드
        self.damage = 8

class SyringeSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/syringe_sword.png')  # 시린지 검 이미지 로드
        self.damage = 8

class BlackpinkSword(Sword):
    def __init__(self, character):
        Sword.__init__(self,character)
        self.image = load_image('sword/blackpink_sword.png')  # 블랙핑크 검 이미지 로드
        self.damage = 10



