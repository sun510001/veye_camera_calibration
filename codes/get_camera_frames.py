'''
Author: sun510001 sqf121@gmail.com
Date: 2024-05-29 21:37:55
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-02 16:58:27
FilePath: /camera/codes/get_camera_frames.py
Description: Loading camera from /dev/video0, but script can only record camera by 1080p15fps
'''

import os
import time
import cv2

# print(cv2.__version__)
# print(cv2.getBuildInformation())

def get_current_time():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


def load_camera(cam_height, cam_width, gstreamer_pipeline, save_folder, framerate):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)
        
    if not cap.isOpened():
        print("Failed to open video device")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
    
    window_name = "camera"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, int(cam_width//3), int(cam_height//3))
    
    frame_num = 0
    in_recording = False

    start_time = cv2.getTickCount()
    
    try:
        while True:
            # read the frame
            ret, frame = cap.read() 
            if ret:
                frame_num += 1
                frame = cv2.flip(frame,1)
                
                frame_draw = frame.copy()
                
                if in_recording:
                    cv2.circle(frame_draw, (50, 50), 20, (0, 0, 255), -1)
                    out.write(frame)
                    
                ###########
                # Control the recording speed, wait for a certain amount of time to achieve the purpose of reducing the recording speed.
                elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
                wait_time = int(1000/30 - elapsed_time * 1000)
                if wait_time > 0:
                    press_key = cv2.waitKey(wait_time) & 0xFF
                    print("Loop to fast, need waiting:", wait_time)
                else:
                    press_key = cv2.waitKey(1) & 0xFF
                ###########
                             
                cv2.imshow(window_name, frame_draw)
                print(f"Frame: {frame_num}, wxh: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}, fps: {cap.get(5)}")
            else:
                print("Failed to read frame")
                break
            
            # press_key = cv2.waitKey(1) & 0xFF
            
            if press_key == ord('q'):
                break
            elif press_key == ord('c'):
                    file_path = os.path.join(save_folder, f"capture_{get_current_time()}.jpg")
                    cv2.imwrite(file_path, frame)
                    print("################### Captured ##################")
            elif press_key == ord('r'):
                    if not in_recording:
                        print("################### Recording started ##################")
                        in_recording = True
                        file_path = os.path.join(save_folder, f"capture_{get_current_time()}.mp4")
                        out = cv2.VideoWriter(file_path, fourcc, cap.get(5), (cam_width, cam_height))
                        out.write(frame)
                    else:
                        out.release()
                        in_recording = False
                        print("################### Recording ended ##################")
                        
    except KeyboardInterrupt:
        # ctrl-c to stop
        pass
            
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        
        # 关闭GStreamer管道
        if in_recording:
            out.release()
            print("################### Recording ended ##################")

        
def main():
    cam_height = 1080
    cam_width = 1920
    framerate = 15

    max_size_buffer = 1  # The smaller the number, the stronger the real-time performance of the image queue.
    device = "/dev/video0"
        
    # enable to save video and image if save_folder != ""
    save_folder = "../data"
    os.makedirs(save_folder, exist_ok=True)


    gstreamer_pipeline_lowfps = (
        f"v4l2src device={device} ! "
        f"queue max-size-buffers={max_size_buffer} leaky=downstream ! "
        f"video/x-raw, format=(string)UYVY, width={cam_width}, height={cam_height}, framerate={framerate}/1 ! "
        "videoconvert ! "
        "appsink"
    )
    load_camera(cam_height, cam_width, gstreamer_pipeline_lowfps, save_folder, framerate)


if __name__=="__main__":
    main()