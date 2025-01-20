import time, cv2
from threading import Thread
from djitellopy import Tello



tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()
keepRecording = True

print(f"배터리 잔량: {tello.get_battery()}%")

response = tello.connect()
if not response:
    print("Tello 연결 실패")
    exit(1)


def videoRecorder():
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)
    video.release()