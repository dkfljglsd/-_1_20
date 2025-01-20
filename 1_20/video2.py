import time
import cv2
from threading import Thread
from djitellopy import Tello

def videoRecorder(frame_read, keep_recording):
    # 비디오 프레임 크기 가져오기
    height, width, _ = frame_read.frame.shape
    # 비디오 라이터 설정
    video = cv2.VideoWriter('video.avi', 
                           cv2.VideoWriter_fourcc(*'XVID'), 
                           30, 
                           (width, height))
    
    while keep_recording():
        # 프레임 쓰기
        video.write(frame_read.frame)
        time.sleep(1/30)
    
    # 완료 후 비디오 파일 닫기
    video.release()

def main():
    # Tello 초기화 및 연결
    tello = Tello()
    
    try:
        # Tello 연결
        tello.connect()
        print(f"배터리 잔량: {tello.get_battery()}%")
        
        # 비디오 스트림 시작
        tello.streamon()
        frame_read = tello.get_frame_read()
        
        # 녹화 상태 관리
        recording = True
        def keep_recording():
            return recording
        
        # 비디오 녹화 쓰레드 시작
        recorder = Thread(target=videoRecorder, 
                         args=(frame_read, keep_recording))
        recorder.start()
        
        # 메인 프로그램 실행 (예: 10초 동안 녹화)
        print("녹화를 시작합니다...")
        time.sleep(10)
        
        # 녹화 종료
        recording = False
        recorder.join()
        print("녹화가 완료되었습니다.")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
    
    finally:
        # 정리
        tello.streamoff()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()