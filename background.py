from pico2d import *

class Background:
    bgm = None

    def __init__(self, image_name):
        self.image = load_image(image_name)
        self.bgm = load_music('sound/bgm.mp3')
        if not Background.bgm:
            Background.bgm = load_music('sound/bgm.mp3')
            Background.bgm.set_volume(100)

    def play_bgm(self):
        """BGM 재생 메서드 - play_mode에서만 호출"""
        if Background.bgm:
            Background.bgm.repeat_play()

    def stop_bgm(self):
        """BGM 정지 메서드"""
        if Background.bgm:
            Background.bgm.stop()

    def update(self):
        pass

    def draw(self):
        import play_mode
        img_height = 1920

        # 카메라 위치에 따라 이미지가 얼마나 내려가야 하는지 계산
        scroll_y = int(play_mode.camera_y) % img_height

        # --- 이미지 두 장을 위아래로 이어 그리기 ---

        # 1. 아래쪽 이미지 (현재 화면에 보이는 메인 배경)
        # 화면상의 중심 좌표 = (이미지 절반 높이) - (스크롤된 양)
        y1 = (img_height // 2) - scroll_y - 120
        self.image.draw(240, y1, 720, img_height)



class Background2(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_04_03.png")

class Background3(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_06_02.png")

class Background4(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_10_02.png")

class Background5(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_02_04.png")

class  Background6(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_03_04.png")

class Background7(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_03_04(Night).png")

class Background8(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_03_04(Noon).png")

class Background9(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_04_03.png")

class Background10(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_04_03(Dusts).png")

class Background11(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_04_03(Night).png")

class Background12(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_05_01(Mist).png")

class Background13(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_05_01(Night).png")

class Background14(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_05_01.png")

class Background15(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_05_02(Evening).png")

class Background16(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_05_02(Night).png")

class Background17(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_05_02(Mist).png")

class Background18(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_05_02.png")

class Background19(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_06_02.png")

class Background20(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_10.png")

class Background21(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_10_02.png")

class Background22(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_10_03(dawn).png")

class Background23(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_10_03(dirty).png")

class Background24(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_10_03(evening).png")

class Background25(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_10_03(Mists).png")

class Background26(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_11.png")

class Background27(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_11_02(dawn).png")

class Background28(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_11_02(fall_sky).png")

class Background29(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_11_02(night_deep).png")

class Background30(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_12(Evening).png")

class Background31(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_12(Mists).png")

class Background32(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_12(night).png")

class Background33(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_12.png")

class Background34(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_13(Mars).png")

class Background35(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_13(Mars with Earth).png")

class Background36(Background):
    def __init__(self):
        Background.__init__ (self,"background/Background_13(Moon).png")

