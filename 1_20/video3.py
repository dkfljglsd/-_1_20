import time
import cv2
from threading import Thread
from djitellopy import Tello

def videoRecorder(frame_read, keep_recording):
    # 프레임을 받을 때까지 잠시 대기
    time.sleep(2)
    
    # 비디오 프레임 크기 가져오기
    height, width, _ = frame_read.frame.shape
    # 비디오 라이터 설정
    video = cv2.VideoWriter('video.avi', 
                           cv2.VideoWriter_fourcc(*'XVID'), 
                           30, 
                           (width, height))
    
    print("녹화를 시작합니다...")
    
    while keep_recording():
        # 프레임 쓰기
        video.write(frame_read.frame)
        # 화면에 프레임 표시 (녹화 확인용)
        cv2.imshow('Tello 영상', frame_read.frame)
        
        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        time.sleep(1/30)
    
    # 완료 후 비디오 파일 닫기
    video.release()
    print("녹화가 완료되었습니다.")

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
        
        # 사용자가 'q'를 누를 때까지 계속 녹화
        print("녹화를 종료하려면 'q'를 누르세요...")
        while recording:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                recording = False
                break
            time.sleep(0.1)
        
        # 녹화 종료
        recorder.join()
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
    
    finally:
        # 정리
        tello.streamoff()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()