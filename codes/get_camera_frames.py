'''
Author: sun510001 sqf121@gmail.com
Date: 2024-05-29 21:37:55
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-01 10:51:21
FilePath: /camera/codes/get_camera_frames.py
Description: Loading camera from /dev/video0
'''

import cv2
# print(cv2.__version__)
# print(cv2.getBuildInformation())

def load_camera(cam_height, cam_width, gstreamer_pipeline):
    cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Failed to open video device")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
    
    window_name = "camera"
    # 创建一个具有固定大小的窗口
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, cam_width//3, cam_height//3)
    
    frame_num = 0
    while True:
        ret, frame = cap.read()
        if ret:
            frame_num += 1
            # Display the frame
            cv2.imshow(window_name, frame)
            print(f"Frame: {frame_num}, wxh: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}, fps: {cap.get(5)}")
        else:
            print("Failed to read frame")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Release resources
    cap.release()
    cv2.destroyAllWindows()


def main():
    cam_height = 1080
    cam_width = 1920
    framerate = 30
    max_size_buffer = 1  # 图片最大队列, 数字越小实时性越强
    device = "/dev/video0"
    
    gstreamer_pipeline = (
        f"v4l2src device={device} ! "
        f"queue max-size-buffers={max_size_buffer} leaky=downstream ! "
        f"video/x-raw, format=(string)UYVY, width={cam_width}, height={cam_height}, framerate={framerate}/1 ! "
        "videoconvert ! "
        "appsink"
    )
    load_camera(cam_height, cam_width, gstreamer_pipeline)


if __name__=="__main__":
    main()