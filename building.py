from pico2d import *
import random

# Building의 부모클래스 정의
class Building:
    def __init__(self, image_file='Building1.png', num_floors=9): # 기본 건물 이미지 파일과 층 수
        self.x, self.y = 200, 1000  # 건물의 초기 위치
        self.building = load_image(image_file)  # 건물 이미지 로드
        self.framex = 450  # 건물 프레임 크기 x
        self.framey = 100  # 건물 프레임 크기 y

        # 층 정보 초기화
        self.floors = []
        for i in range(num_floors): # 각 층에 대한 정보 저장 (부모클래스 이기 때문)
            self.floors.append({
                'clip_y': i * 307, # 각 층의 클립 y 위치
                'y_offset': i * 101, # 각 층의 y 오프셋
                'alive': True # 층이 살아있는지 여부
            })

        self.num_floors = num_floors # 층 수 저장

    def update(self):
        # 각 층이 개별적으로 바닥(y=20)으로 내려옴
        for floor in self.floors:
            if floor['alive']: # 만약 floor가 살아있다면 = 파괴되지 않았다면 = True라면
                target_y = 20  # 목표 y 위치
                current_y = self.y + floor['y_offset']
                if current_y > target_y:
                    floor['y_offset'] -= 0.5  # 각 층이 개별적으로 내려옴

    # 층 파괴 함수
    def destroy_floor(self, floor_num):
        if 0 <= floor_num < len(self.floors):
            self.floors[floor_num]['alive'] = False # 해당 층을 파괴 상태로 변경
            print(f"{floor_num + 1}층 파괴됨!")

    def draw(self):
        # 살아있는 층만 그리기
        for floor in self.floors:
            if floor['alive']:
                self.building.clip_draw(0, floor['clip_y'], 1080, 307,
                                        self.x, self.y + floor['y_offset'],
                                        self.framex, self.framey)
            # 충돌 박스 함수들
        for i in range(self.num_floors): # 9층 건물
            bb = self.get_bb_floor(i) # 각 층의 충돌 박스 가져오기
            if bb: # 충돌 박스가 존재하면
                draw_rectangle(*bb) # 충돌 박스 그리기

    def get_bb_floor(self, floor_num):
        if not self.floors[floor_num]['alive']: # 층이 파괴되었으면
            return None # 충돌 박스 없음
        floor_y = self.y + self.floors[floor_num]['y_offset'] # 층의 현재 y 위치 계산
        return self.x - 225, floor_y - 50, self.x + 225, floor_y + 50 # 충돌 박스 좌표 반환

    # 기존 get_bb_floor1~9 메서드들 (호환성 유지)
    def get_bb_floor1(self): return self.get_bb_floor(0)
    def get_bb_floor2(self): return self.get_bb_floor(1)
    def get_bb_floor3(self): return self.get_bb_floor(2)
    def get_bb_floor4(self): return self.get_bb_floor(3)
    def get_bb_floor5(self): return self.get_bb_floor(4)
    def get_bb_floor6(self): return self.get_bb_floor(5)
    def get_bb_floor7(self): return self.get_bb_floor(6)
    def get_bb_floor8(self): return self.get_bb_floor(7)
    def get_bb_floor9(self): return self.get_bb_floor(8)

# 빌딩의 자식 클래스 (빌딩 자식 클래스의 숫자는 파일의 숫자와 같게 함)
class Building52(Building):
    def __init__(self):
        super().__init__('Building52.png',num_floors=7)  # 부모의 __init__ 호출
        print("자식 클래스 초기화 완료") # 디버그 메시지

class Building41(Building):
    def __init__(self):
        super().__init__('Building41.png',num_floors=11)  # 부모의 __init__ 호출
        print("자식 클래스 초기화 완료") # 디버그 메시지
def create_random_building():
    buildings = [Building, Building52, Building41]
    return random.choice(buildings)()