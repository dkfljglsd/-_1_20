import time
import cv2
from threading import Thread
from djitellopy import Tello

try:
    # Tello 초기화 및 연결
    tello = Tello()
    tello.connect()  # connect() 호출 후 성공/실패 확인하지 않음
    
    print(f"배터리 잔량: {tello.get_battery()}%")
    
    # 비디오 스트림 시작
    tello.streamon()
    frame_read = tello.get_frame_read()
    
    # 녹화 상태
    keepRecording = True
    
    def videoRecorder():
        # 프레임 크기 가져오기
        height, width, _ = frame_read.frame.shape
        
        # 비디오 설정
        video = cv2.VideoWriter(
            'video.avi',
            cv2.VideoWriter_fourcc(*'XVID'),
            30,
            (width, height)
        )
        
        print("녹화를 시작합니다...")
        
        while keepRecording:
            # 프레임 녹화
            video.write(frame_read.frame)
            
            # 화면에 영상 표시
            cv2.imshow("Tello Video", frame_read.frame)
            
            # q 키로 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            time.sleep(1/30)
        
        # 비디오 파일 저장
        video.release()
        print("녹화가 완료되었습니다.")
    
    # 녹화 쓰레드 시작
    recorder = Thread(target=videoRecorder)
    recorder.start()
    
    print("녹화를 종료하려면 'q'를 누르세요...")
    
    # 메인 루프
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            keepRecording = False
            break
        time.sleep(0.1)

except Exception as e:
    print(f"오류가 발생했습니다: {str(e)}")
    
finally:
    # 정리
    keepRecording = False
    cv2.destroyAllWindows()
    tello.streamoff()
    
    # 쓰레드가 존재하면 종료 대기
    if 'recorder' in locals() and recorder.is_alive():
        recorder.join()