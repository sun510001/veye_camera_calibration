"""
Author: sqf
Date: 2024-06-08 20:35:35
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-08 23:53:24
FilePath: /veye_camera_calibration/codes/dual_camera_image_acquire.py
Description: Use a high-precision clock to send signals to the dual camera to achieve software synchronization.

Copyright (c) 2024 by sqf, All Rights Reserved. 
"""

import threading
import time
import cv2
from queue import Queue, Empty


capture_event = threading.Event()
image_queue = Queue()
sync_frame = 0


def capture_image(cap):
    ret, frame = cap.read()
    if ret is None:
        print("Capture image failed.")
        return None

    return frame


def capture_scheduler(interval):
    global sync_frame
    while True:
        time.sleep(interval)
        capture_event.set()
        capture_event.clear()
        sync_frame += 1


def capture_camera(cam_idx, gstreamer_pipeline, set_width, set_height, image_queue):
    cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Failed to open video device", "cam", cam_idx)
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, set_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, set_height)

    framerate_get = cap.get(5)
    print("Current fps: %d fps" % framerate_get)

    while True:
        capture_event.wait()
        image = capture_image(cap)
        if image is not None:
            image_queue.put([image, cam_idx, sync_frame])


def display_images(image_queue):
    frame_dict = {}
    current_frame_num = 0
    while True:
        try:
            image, cam_idx, frame_num = image_queue.get(timeout=1)
            if frame_num == current_frame_num:
                if frame_num not in frame_dict:
                    frame_dict[frame_num] = {}
                frame_dict[frame_num][cam_idx] = image

                if len(frame_dict[frame_num]) == 2:  # 当两张图片都到达时
                    combined_image = cv2.hconcat(
                        [frame_dict[frame_num][0], frame_dict[frame_num][1]]
                    )
                    cv2.imshow("Combined Image", combined_image)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    del frame_dict[frame_num]  # 移除已显示的帧
                    current_frame_num += 1  # 处理下一帧
            else:
                # 丢弃过期帧
                while frame_num > current_frame_num:
                    current_frame_num += 1
                    if current_frame_num in frame_dict:
                        del frame_dict[current_frame_num]
        except Empty:
            continue

    cv2.destroyAllWindows()


def start_image_capturing(
    gstreamer_pipeline_list,
    set_width,
    set_height,
    interval,
):
    thread_list = []
    for cam_idx, gs_pipline in enumerate(gstreamer_pipeline_list):
        thread = threading.Thread(
            target=capture_camera,
            args=(
                cam_idx,
                gs_pipline,
                set_width,
                set_height,
                image_queue,
            ),
        )
        thread.start()
        thread_list.append(thread)

    scheduler_thread = threading.Thread(target=capture_scheduler, args=(interval,))
    scheduler_thread.start()

    save_thread = threading.Thread(
        target=display_images,
        args=(image_queue,),
    )
    save_thread.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        for thread in thread_list:
            thread.join()
        scheduler_thread.join()
        save_thread.join()
        print("All threads have been terminated.")


def main():
    set_width = 1920
    set_height = 1080
    interval = 1 / 15  # capture interval
    camera_dev_list = ["/dev/video8", "/dev/video0"]  # camera device index
    max_size_buffer = 1

    gstreamer_pipeline_list = []
    for dev in camera_dev_list:
        gstreamer_pipeline_list.append(
            (
                f"v4l2src device={dev} ! "
                f"queue max-size-buffers={max_size_buffer} leaky=downstream ! "
                f"video/x-raw, format=(string)UYVY, width={set_width}, height={set_height}, framerate={int(1/interval)}/1 ! "
                "videoconvert ! "
                "appsink"
            )
        )

    start_image_capturing(gstreamer_pipeline_list, set_width, set_height, interval)


if __name__ == "__main__":
    main()
