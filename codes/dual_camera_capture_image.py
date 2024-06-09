"""
Author: sqf
Date: 2024-06-08 20:35:35
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-08 23:53:24
FilePath: /veye_camera_calibration/codes/dual_camera_image_acquire.py
Description: Use a high-precision clock to send signals to the dual camera to achieve software synchronization
and save images

Copyright (c) 2024 by sqf, All Rights Reserved. 
"""

import os
import threading
import time
import datetime
import cv2
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor

# 定义全局事件，用于控制采图指令的发送
capture_event = threading.Event()
# 定义图像队列
image_queue = Queue()
sync_frame = 0  # 用于存储需要传递的变量


def capture_image(cap):
    # 获取一帧图像
    ret, frame = cap.read()
    if ret is None:
        print("Capture image failed.")
        return None

    return frame


def capture_scheduler(interval):
    global sync_frame
    while True:
        time.sleep(interval)
        capture_event.set()  # 发送采图指令
        capture_event.clear()  # 清除事件，为下次采图做准备
        sync_frame += 1


def capture_camera(cam_idx, gstreamer_pipeline, set_width, set_height, image_queue):

    # 通过索引打开设备
    cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Failed to open video device", "cam", cam_idx)
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, set_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, set_height)

    framerate_get = cap.get(5)
    print("Current fps: %d fps" % framerate_get)

    while True:
        capture_event.wait()  # 等待采图指令
        image = capture_image(cap)
        if image is not None:
            image_queue.put([image, cam_idx, sync_frame])


def save_images(image, cam_idx, sync_frame, save_image_folder):
    image_path = os.path.join(save_image_folder, f"{sync_frame:08}_cam{cam_idx}.jpg")
    cv2.imwrite(image_path, image)


def save_images_periodically(
    image_queue, save_interval, save_image_folder, max_workers
):
    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:  # 增加线程池中的工作线程数
        while True:
            time.sleep(save_interval)
            images_to_save = []
            while not image_queue.empty():
                try:
                    images_to_save.append(image_queue.get_nowait())
                except Empty:
                    break
            if images_to_save:
                for [image, cam_idx, sync_frame] in images_to_save:
                    executor.submit(
                        save_images, image, cam_idx, sync_frame, save_image_folder
                    )
            print(f"Queue size after saving: {image_queue.qsize()}")


def start_image_capturing():
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
        target=save_images_periodically,
        args=(
            image_queue,
            save_interval,
            save_image_folder,
            max_workers,
        ),
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
    mtime = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    save_image_folder = f"data/sync_{mtime}"  # 设置保存的文件夹

    set_width = 1920
    set_height = 1080
    interval = 1 / 15  # 定时器间隔（秒）
    save_interval = 1.0  # 保存间隔（秒）
    camera_dev_list = ["/dev/video8", "/dev/video0"]  # 相机索引编号
    max_workers = 1
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

    os.makedirs(save_image_folder, exist_ok=True)

    ##################################
    start_image_capturing()


if __name__ == "__main__":
    main()
