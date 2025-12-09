from pico2d import *
import random, game_framework, game_world

class PauseMenu:
    def __init__(self):
        self.image_restart = load_image("ui/Button_06.png") # 재시작 이미지
        self.image_quit = load_image("ui/Button_07.png") # 나가기 이미지

        # 버튼 위치 및 크기 설정
        self.center_x = 240
        self.center_y = 360

        # 버튼 크기
        self.button_size = 100 # 버튼 크기
        self.spacing = 80  # 버튼 간 간격

        # 재시작 버튼 위치
        self.restart_button_x = self.center_x - self.spacing
        self.restart_button_y = self.center_y

        # 나가기 버튼 위치
        self.quit_button_x = self.center_x + self.spacing
        self.quit_button_y = self.center_y

    def update(self):
        pass

    def draw(self):
        self.image_restart.draw(self.restart_button_x, self.restart_button_y, self.button_size, self.button_size)
        self.image_quit.draw(self.quit_button_x, self.quit_button_y, self.button_size, self.button_size)

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.x, 720 - event.y  # 마우스 좌표 변환

            # 재시작 버튼 클릭 여부 확인
            if (self.restart_button_x - self.button_size / 2 <= mouse_x <= self.restart_button_x + self.button_size / 2 and
                self.restart_button_y - self.button_size / 2 <= mouse_y <= self.restart_button_y + self.button_size / 2):
                return 'restart'  # 재시작 이벤트 반환

            # 나가기 버튼 클릭 여부 확인
            if (self.quit_button_x - self.button_size / 2 <= mouse_x <= self.quit_button_x + self.button_size / 2 and
                self.quit_button_y - self.button_size / 2 <= mouse_y <= self.quit_button_y + self.button_size / 2):
                return 'quit'  # 나가기 이벤트 반환

        return None


class Debris:
    # 이미지와 해당 이미지 내의 파편 좌표들(Left, Bottom, Width, Height)을 정의
    # (Pico2D는 좌하단이 (0,0)입니다. 그림판 등에서 좌표를 확인해야 함)
    # 아래 좌표는 예시로 대략적으로 잡은 것입니다. 실제 이미지에 맞춰 조정이 필요할 수 있습니다.
    TYPE_DATA = {
        'ui/wreck.png': [
            (3, 26, 61, 730), (117, 1, 185, 63),
            (69, 43, 124, 99), (127, 70, 183, 134),
            (24, 118, 99, 175), (107, 139, 183, 196)
        ],
        'ui/wreck2.png': [
            (3, 26, 61, 730), (117, 1, 185, 63),
            (69, 43, 124, 99), (127, 70, 183, 134),
            (24, 118, 99, 175), (107, 139, 183, 196)
        ],
        'ui/fragment.png': [
            (335, 41, 559, 231), (26,38,238,235),
            (41, 357, 266, 497)
        ]
    }

    images = {}  # 이미지를 한 번만 로딩하기 위한 딕셔너리

    def __init__(self, x, y):
        # 1. 사용할 이미지 키(파일명)를 랜덤 선택
        self.image_key = random.choice(list(Debris.TYPE_DATA.keys()))

        # 2. 이미지 로딩 (없으면 로드해서 저장)
        if self.image_key not in Debris.images:
            Debris.images[self.image_key] = load_image(self.image_key)

        self.image = Debris.images[self.image_key]

        # 3. 해당 이미지 내에서 랜덤한 파편 조각(Rect) 선택
        # (left, bottom, width, height)
        self.rect = random.choice(Debris.TYPE_DATA[self.image_key])

        self.x, self.y = x, y

        # 물리 및 회전 속성
        self.dx = random.uniform(-200, 200)
        self.dy = random.uniform(200, 500)
        self.gravity = 1200

        self.angle = random.uniform(0, 360)  # 현재 각도 (라디안 변환 필요)
        self.rotate_speed = random.uniform(-5, 5)  # 회전 속도 (라디안/초)

        self.scale = random.uniform(0.8, 1.2)  # 크기 배율
        self.timer = 0.0
        self.life_time = 1.5

    def update(self):
        self.timer += game_framework.frame_time
        if self.timer >= self.life_time:
            game_world.remove_object(self)
            return

        self.x += self.dx * game_framework.frame_time
        self.y += self.dy * game_framework.frame_time
        self.dy -= self.gravity * game_framework.frame_time

        self.angle += self.rotate_speed * game_framework.frame_time

    def draw(self):
        import play_mode
        screen_y = self.y - play_mode.camera_y

        if -50 < screen_y < 800:
            # clip_composite_draw 사용
            # 인자 순서: (잘라낼L, 잘라낼B, 잘라낼W, 잘라낼H, 회전각도, 좌우반전여부, 화면X, 화면Y, 그릴W, 그릴H)

            rx, ry, rw, rh = self.rect  # 선택된 파편의 좌표와 크기

            # 그릴 크기는 원본 크기 * 스케일
            draw_w = rw * self.scale
            draw_h = rh * self.scale

            self.image.clip_composite_draw(
                rx, ry, rw, rh,  # 이미지에서 잘라낼 부분
                self.angle, '',  # 회전 각도 및 반전 없음
                self.x, screen_y,  # 화면 위치
                draw_w, draw_h  # 화면에 그려질 크기
            )

    def get_bb(self):
        return None


def create_debris(x, y, count=10):
    for _ in range(count):
        debris = Debris(x, y)
        game_world.add_object(debris, 1)