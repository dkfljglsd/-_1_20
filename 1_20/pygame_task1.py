from djitellopy import Tello
import pygame
import time

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tello Drone Control")

# 드론 객체 생성 및 연결
tello = Tello()
tello.connect()
print(f"배터리 잔량: {tello.get_battery()}%")

# 키 매핑
KEY_MAPPING = {
    pygame.K_w: lambda: tello.move_forward(30),  # 전진
    pygame.K_s: lambda: tello.move_back(30),     # 후진
    pygame.K_a: lambda: tello.move_left(30),     # 좌측 이동
    pygame.K_d: lambda: tello.move_right(30),    # 우측 이동
    pygame.K_r: lambda: tello.move_up(30),       # 상승
    pygame.K_f: lambda: tello.move_down(30),     # 하강
    pygame.K_e: lambda: tello.rotate_clockwise(30),  # 시계 방향 회전
    pygame.K_q: lambda: tello.rotate_counter_clockwise(30),  # 반시계 방향 회전
}

# 드론 이륙
tello.takeoff()

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창 닫기 버튼 처리
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC 키: 종료
                running = False
            elif event.key in KEY_MAPPING:
                try:
                    KEY_MAPPING[event.key]()  # 매핑된 명령 실행
                    time.sleep(2)  # 명령 간 대기
                except Exception as e:
                    print(f"명령 실행 중 오류: {e}")

# 드론 착륙 및 종료
tello.land()
pygame.quit()
