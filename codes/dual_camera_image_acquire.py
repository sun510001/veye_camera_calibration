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
image_queue = Queue(maxsize=2)
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


def capture_camera(cam_idx, gstreamer_pipeline, set_width, set_height):
    global image_queue, sync_frame
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


def request_images(width, height, show_size, show_image_realtime):
    global image_queue
    cam_images = {}
    resize_size = (int(width * show_size), int(height * show_size))

    windows_name = "Combined Image"
    cv2.namedWindow(windows_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windows_name, int(width * show_size * 2), int(height * show_size))
    # frame_count = 0
    while True:
        try:
            image, cam_idx, sync_frame_ = image_queue.get_nowait()
            cam_images[cam_idx] = image
            # print(cam_idx, sync_frame_)

            if len(cam_images) == 2:
                # process images
                if show_image_realtime:
                    image_left = cv2.resize(cam_images[0], resize_size)
                    image_right = cv2.resize(cam_images[1], resize_size)
                    combined_image = cv2.hconcat([image_left, image_right])
                    cv2.imshow("Combined Image", combined_image)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                cam_images.clear()
        except Empty:
            print("Empty ...")
            continue

    if show_image_realtime:
        cv2.destroyAllWindows()


def start_image_request(
    gstreamer_pipeline_list,
    set_width,
    set_height,
    show_size,
    interval,
    show_image_realtime,
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

    request_images_thread = threading.Thread(
        target=request_images,
        args=(set_width, set_height, show_size, show_image_realtime),
    )
    request_images_thread.start()

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
        print("Scheduler thread is terminated.")
        request_images_thread.join()
        print("Request thread is terminated.")
        print("All threads have been terminated.")


def main():
    set_width = 1920
    set_height = 1080
    interval = 1 / 15  # capture interval
    camera_dev_list = [
        "/dev/video8",
        "/dev/video0",
    ]  # camera device index; /dev/video8 left; /dev/video0 right
    max_size_buffer = 1
    show_size = 0.5  # show image with 1/2 size
    show_image_realtime = True

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

    start_image_request(
        gstreamer_pipeline_list,
        set_width,
        set_height,
        show_size,
        interval,
        show_image_realtime,
    )


if __name__ == "__main__":
    main()
