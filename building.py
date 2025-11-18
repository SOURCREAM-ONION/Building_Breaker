from pico2d import *


class Building:
    def __init__(self):
        self.x, self.y = 200, 500  # 건물의 초기 위치
        self.building = load_image('Building1.png')  # 건물 이미지 로드
        self.framex = 450  # 건물 프레임 크기 x
        self.framey = 100  # 건물 프레임 크기 y

        # 각 층 정보를 append로 추가 (alive 추가)
        self.floors = []
        self.floors.append({'clip_y': 307, 'y_offset': 0, 'alive': True})  # 1층
        self.floors.append({'clip_y': 614, 'y_offset': 101, 'alive': True})  # 2층
        self.floors.append({'clip_y': 921, 'y_offset': 202, 'alive': True})  # 3층

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        # 각 층이 개별적으로 바닥(y=20)으로 내려옴
        for floor in self.floors:
            if floor['alive']:
                target_y = 20  # 목표 y 위치
                current_y = self.y + floor['y_offset']

                if current_y > target_y:
                    floor['y_offset'] -= 0.5  # 각 층이 개별적으로 내려옴

    def do(self):
        pass

    def get_bb(self):
        return self.x - 200, self.y - 15, self.x + 200, self.y + 325  # 건물의 충돌 박스 좌표 반환

    # 1층 충돌 박스
    def get_bb_floor1(self):
        if not self.floors[0]['alive']:
            return None
        floor_y = self.y + self.floors[0]['y_offset']
        return self.x - 225, floor_y - 50, self.x + 225, floor_y + 50

    # 2층 충돌 박스
    def get_bb_floor2(self):
        if not self.floors[1]['alive']:
            return None
        floor_y = self.y + self.floors[1]['y_offset']
        return self.x - 225, floor_y - 50, self.x + 225, floor_y + 50

    # 3층 충돌 박스
    def get_bb_floor3(self):
        if not self.floors[2]['alive']:
            return None
        floor_y = self.y + self.floors[2]['y_offset']
        return self.x - 225, floor_y - 50, self.x + 225, floor_y + 50

    # 층 파괴 함수
    def destroy_floor(self, floor_num):
        if 0 <= floor_num < len(self.floors):
            self.floors[floor_num]['alive'] = False
            print(f"{floor_num + 1}층 파괴됨!")

    def draw(self):
        # 살아있는 층만 그리기
        for floor in self.floors:
            if floor['alive']:
                self.building.clip_draw(0, floor['clip_y'], 1080, 307,
                                        self.x, self.y + floor['y_offset'],
                                        self.framex, self.framey)

        # 살아있는 층의 충돌 박스만 그리기
        if self.floors[0]['alive']:
            draw_rectangle(*self.get_bb_floor1())  # 1층
        if self.floors[1]['alive']:
            draw_rectangle(*self.get_bb_floor2())  # 2층
        if self.floors[2]['alive']:
            draw_rectangle(*self.get_bb_floor3())  # 3층