import cv2
import time
from djitellopy import Tello

def main():
    # Initialize Tello
    tello = Tello()
    
    try:
        # Connect to Tello
        tello.connect()
        print("Connected to Tello")
        
        # Turn on video stream
        tello.streamon()
        print("Video stream started")
        
        # Get the frame read object
        frame_read = tello.get_frame_read()
        
        # Take off
        tello.takeoff()
        print("Takeoff successful")
        
        # Wait a moment to stabilize
        time.sleep(3)
        
        # Take a picture
        cv2.imwrite("picture.png", frame_read.frame)
        print("Picture taken")
        
        # Land
        tello.land()
        print("Landed successfully")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Make sure we land if something goes wrong
        tello.land()
    
    finally:
        # Cleanup
        cv2.destroyAllWindows()
        tello.streamoff()

if __name__ == "__main__":
    main()