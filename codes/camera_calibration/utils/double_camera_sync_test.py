"""
Author: sqf
Date: 2024-06-09 15:49:40
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-10 20:28:51
FilePath: /veye_camera_calibration/codes/camera_calibration/utils/double_camera_sync_test.py
Description: Verify the synchronization of the dual cameras by stitching the two images together for display.

Copyright (c) 2024 by sqf, All Rights Reserved. 
"""

import os
import cv2
import numpy as np
from glob import glob


def match_images(images_path):
    pairs = []
    for image in images_path:
        if "cam0" in image and os.path.exists(image.replace("cam0", "cam1")):
            pairs.append([image, image.replace("cam0", "cam1")])
    return pairs


def merge_image_pair(pairs):
    for [img_1, img_2] in pairs:
        np_img_1 = cv2.imread(img_1)
        np_img_1 = cv2.rotate(np_img_1, 0)
        np_img_2 = cv2.imread(img_2)

        h, w, c = np_img_1.shape
        result = np.hstack(
            [cv2.resize(x, (w // 5, h // 5)) for x in [np_img_1, np_img_2]]
        )

        cv2.imshow("images", result)
        # cv2.waitKey(0)
        press_key = cv2.waitKey(0) & 0xFF
        if press_key == ord("q"):
            break
        cv2.destroyAllWindows()
    cv2.destroyAllWindows()


def main():
    image_folder = "fv-bmp-bolt-tightening/camera_calibration/data/samples_5"
    images = glob(os.path.join(image_folder, "*.jpg"))
    pairs = match_images(images)
    merge_image_pair(pairs)


if __name__ == "__main__":
    main()
