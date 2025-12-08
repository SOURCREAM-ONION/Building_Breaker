from pico2d import *
import random
import game_framework

# 상수 정의
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
DROP_SPEED_KMPH = 35.0  # Km / Hour
DROP_SPEED_MPM = (DROP_SPEED_KMPH * 1000.0 / 60.0)
DROP_SPEED_MPS = (DROP_SPEED_MPM / 60.0)
DROP_SPEED_PPS = (DROP_SPEED_MPS * PIXEL_PER_METER)

# 튕기는 듯한 느낌을 주는 속도 상수
BOUNCE_SPEED_KMPH = 450 # 방어 시 건물이 살짝 튕기는 속도

# Building의 부모클래스 정의
class Building:
    based_foors_hp = 1

    def __init__(self, image_file='building/Building1.png', num_floors=9): # 기본 건물 이미지 파일과 층 수
        self.x, self.y = 240, 2000  # 건물의 초기 위치
        self.building = load_image(image_file)  # 건물 이미지 로드
        self.framex = 480  # 건물 프레임 크기 x
        self.framey = 150  # 건물 프레임 크기 y

        # 층 정보 초기화
        self.floors = []
        for i in range(num_floors): # 각 층에 대한 정보 저장 (부모클래스 이기 때문)
            self.floors.append({
                'clip_y': i * 307, # 각 층의 클립 y 위치
                'y_offset': i * 150, # 각 층의 y 오프셋
                'alive': True, # 층이 살아있는지 여부
                'hp' : Building.based_foors_hp # 각 층의 체력
            })

        self.num_floors = num_floors # 층 수 저장

    def update(self):
        """ 각 층이 개별적으로 바닥(y=20)으로 내려옴
        만약 floor가 파괴되지 않았다면 (alive가 True라면) target_y(20)까지 내려옴, 현재위치는 y값 + 층수의 y값
        for문을 돌려 각 층마다 처리 """
        for floor in self.floors:
            if floor['alive']: # 만약 floor가 살아있다면 = 파괴되지 않았다면 = True라면
                target_y = PIXEL_PER_METER * 2  # 목표 y 위치
                current_y = self.y + floor['y_offset']
                if current_y > target_y:
                    floor['y_offset'] -= DROP_SPEED_PPS * game_framework.frame_time  # 각 층이 개별적으로 내려옴

    def take_damage(self, floor_num, damage):
        if 0 <= floor_num < len(self.floors):
            floor = self.floors[floor_num]
            if floor['alive']:
                floor['hp'] -= damage
                print(f"{floor_num + 1}층이 {damage} 데미지를 입음! 남은 체력: {floor['hp']}")
                if floor['hp'] <= 0:
                    self.destroy_floor(floor_num)

    # 층 파괴 함수
    def destroy_floor(self, floor_num):
        if 0 <= floor_num < len(self.floors):
            self.floors[floor_num]['alive'] = False # 해당 층을 파괴 상태로 변경
            print(f"{floor_num + 1}층 파괴됨!")

    # 건물이 튕겨지는 함수
    def push_up(self):
        # 방어 성공 시 호출: 모든 층을 위로 튕겨 올림
        for floor in self.floors:
            if floor['alive']:
                    floor['y_offset'] += BOUNCE_SPEED_KMPH # 모든 층이 위로 올라감

    def draw(self):
        import play_mode  # 카메라 위치 참조

        # 살아있는 층만 그리기
        for floor in self.floors:
            if floor['alive']:
                # 건물의 월드 y좌표(self.y + offset)에서 카메라 y를 뺌
                screen_y = (self.y + floor['y_offset']) - play_mode.camera_y

                self.building.clip_draw(0, floor['clip_y'], 1080, 307,
                                        self.x, screen_y,
                                        self.framex, self.framey)

        # 충돌 박스 그리기 (디버깅용)
        for i in range(self.num_floors):
            bb = self.get_bb_floor(i)
            if bb:
                l, b, r, t = bb
                # 충돌 박스 좌표도 카메라만큼 내려서 그림
                draw_rectangle(l, b - play_mode.camera_y, r, t - play_mode.camera_y)

    def get_bb_floor(self, floor_num):
        if not self.floors[floor_num]['alive']: # 층이 파괴되었으면
            return None # 충돌 박스 없음
        floor_y = self.y + self.floors[floor_num]['y_offset'] # 층의 현재 y 위치 계산
        return self.x - 250, floor_y - 75, self.x + 250, floor_y + 75 # 충돌 박스 좌표 반환


# 빌딩의 자식 클래스 (빌딩 자식 클래스의 숫자는 파일의 숫자와 같게 함)
class Building52(Building):
    def __init__(self):
        Building.__init__(self,'building/Building52.png', num_floors=7)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("52 자식 클래스 초기화 완료") # 디버그 메시지

class Building41(Building):
    def __init__(self):
        Building.__init__(self,'building/Building41.png', num_floors=11)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("41 자식 클래스 초기화 완료") # 디버그 메시지

class Building33(Building):
    def __init__(self):
        Building.__init__(self,'building/Building33.png', num_floors=7)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("33 자식 클래스 초기화 완료") # 디버그 메시지

class Building4(Building):
    def __init__(self):
        Building.__init__(self,'building/Building4.png', num_floors=11)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("4 자식 클래스 초기화 완료") # 디버그 메시지

class Building32(Building):
    def __init__(self):
        Building.__init__(self,'building/Building32.png', num_floors=7)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("32 자식 클래스 초기화 완료") # 디버그 메시지

class Building2(Building):
    def __init__(self):
        Building.__init__(self,'building/Building2.png', num_floors=11)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("2 자식 클래스 초기화 완료") # 디버그 메시지

class Building5(Building):
    def __init__(self):
        Building.__init__(self,'building/Building5.png', num_floors=9)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("5 자식 클래스 초기화 완료") # 디버그 메시지

class Building10(Building):
    def __init__(self):
        Building.__init__(self,'building/Building10.png', num_floors=9)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("10 자식 클래스 초기화 완료") # 디버그 메시지

class Building12(Building):
    def __init__(self):
        Building.__init__(self,'building/Building12.png', num_floors=9)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("12 자식 클래스 초기화 완료") # 디버그 메시지

class Building13(Building):
    def __init__(self):
        Building.__init__(self,'building/Building13.png', num_floors=9)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("13 자식 클래스 초기화 완료") # 디버그 메시지

class Building45(Building):
    def __init__(self):
        Building.__init__(self,'building/Building45.png', num_floors=10)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("45 자식 클래스 초기화 완료") # 디버그 메시지

class Building46(Building):
    def __init__(self):
        Building.__init__(self,'building/Building46.png', num_floors=10)  # 부모의 __init__ 호출 (super의 기능 = 부모클래스의 메서드 호출)
        print("46 자식 클래스 초기화 완료") # 디버그 메시지

def create_random_building():
    #buildings = [Building,Building41,Building52,Building33,Building4,Building32,Building2,Building5,Building10,Building12,Building13,Building45,Building46]
    buildings = [Building13] # 한개씩 테스트 할 때
    return random.choice(buildings)()