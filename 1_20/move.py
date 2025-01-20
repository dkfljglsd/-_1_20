from djitellopy import Tello
import cv2, math, time

# 드론 객체 생성
tello = Tello()

# 드론 연결
tello.connect()

# 배터리 확인
print(f"배터리 잔량: {tello.get_battery()}%")

tello.takeoff()

while True:
    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)

tello.land()

# # 이륙 
# tello.takeoff()

# # 착륙
# tello.land()

# # 전진 30cm
# tello.move_forward(30)

# # 후진 30cm
# tello.move_back(30)

# # 좌회전 90도
# tello.rotate_counter_clockwise(90)


# # 우회전 90도
# tello.rotate_clockwise(90)

# # 착륙
# tello.land()


