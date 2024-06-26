"""
Author: sqf
Date: 2024-06-08 20:35:35
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-08 23:53:24
FilePath: /veye_camera_calibration/codes/dual_camera_image_acquire.py
Description: Use a high-precision clock to send signals to the dual camera to achieve software synchronization
and save images.

Copyright (c) 2024 by sqf, All Rights Reserved. 
"""

import os
import threading
import time
import datetime
import cv2
from collections import deque
from concurrent.futures import ThreadPoolExecutor

capture_event = threading.Event()
image_queue = deque(maxlen=2)
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
        print("Frame:", sync_frame)


def capture_camera(cam_idx, gstreamer_pipeline, set_width, set_height):
    global image_queue
    cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Failed to open video device", "cam", cam_idx)
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, set_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, set_height)

    framerate_get = cap.get(5)
    print("Current fps: %d fps" % framerate_get)

    while True:
        capture_event.wait()  # waitting for capture signal
        image = capture_image(cap)
        if image is not None:
            image_queue.append([image, cam_idx, sync_frame])


def save_images(image, cam_idx, save_image_folder):
    global sync_frame
    image_path = os.path.join(save_image_folder, f"{sync_frame:08}_cam{cam_idx}.jpg")
    cv2.imwrite(image_path, image)


def save_images_periodically(save_interval, save_image_folder, max_workers):
    global sync_frame, image_queue
    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:  # Increase the number of worker threads in the thread pool.
        while True:
            time.sleep(save_interval)
            images_to_save = []
            while image_queue:
                images_to_save.append(image_queue.popleft())
            if images_to_save:
                for [image, cam_idx, sync_frame] in images_to_save:
                    executor.submit(save_images, image, cam_idx, save_image_folder)


def start_image_capturing(
    gstreamer_pipeline_list,
    set_width,
    set_height,
    interval,
    save_interval,
    save_image_folder,
    max_workers,
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
            ),
        )
        thread.start()
        thread_list.append(thread)

    scheduler_thread = threading.Thread(target=capture_scheduler, args=(interval,))
    scheduler_thread.start()

    save_thread = threading.Thread(
        target=save_images_periodically,
        args=(
            save_interval,
            save_image_folder,
            max_workers,
        ),
    )
    save_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        for t_index, thread in enumerate(thread_list):
            thread.join()
            print(f"Camera thread {t_index} is terminated.")
        scheduler_thread.join()
        print(f"Scheduler thread is terminated.")
        save_thread.join()
        print(f"Request thread is terminated.")
        print("All threads have been terminated.")


def main():
    mtime = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    save_image_folder = (
        f"/home/sun/Desktop/camera/codes/data/sync_{mtime}"  # the folder of images
    )

    set_width = 1920
    set_height = 1080
    interval = 1 / 15  # capture interval
    save_interval = 0.5  # save image interval
    camera_dev_list = [
        "/dev/video8",
        "/dev/video0",
    ]  # camera device index; /dev/video8 left; /dev/video0 right
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

    start_image_capturing(
        gstreamer_pipeline_list,
        set_width,
        set_height,
        interval,
        save_interval,
        save_image_folder,
        max_workers,
    )


if __name__ == "__main__":
    main()
