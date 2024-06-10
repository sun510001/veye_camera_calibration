"""
Author: sqf
Date: 2024-06-09 15:55:07
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-09 16:06:34
FilePath: /veye_camera_calibration/codes/camera_calibration/camera_calib_dist.py
Description: 

Copyright (c) 2024 by sqf, All Rights Reserved. 
"""

import cv2
import os
from glob import glob
from utils.camera_calibration import (
    load_img,
    calibrate_camera_by_charuco,
    calibrate_camera_by_chessboard,
)


def main():
    frame_folder = "/home/sun/Desktop/codes/veye_camera_calibration/codes/camera_calibration/data/video8_capture_2024-06-09_16-41-35"
    mode = 1  # 0: charuco; 1: chessboard

    np_imgs, _ = load_img(frame_folder)

    if mode == 0:
        H = 9
        W = 14
        ARUCO_DICT = cv2.aruco.DICT_6X6_250
        SQUARE_LENGTH = 0.015  # Chessboard square side in meters
        MARKER_LENGTH = 0.011  # aruco marker side in meters
        BOARD_CORNERS_SHAPE = (H, W)  # Number of X, Y corners,
        if len(glob(os.path.join(frame_folder, "*.npz"))) == 0:
            calibrate_camera_by_charuco(
                np_imgs,
                ARUCO_DICT,
                BOARD_CORNERS_SHAPE,
                SQUARE_LENGTH,
                MARKER_LENGTH,
                frame_folder,
            )
    elif mode == 1:
        H = 7 - 1
        W = 10 - 1
        SQUARE_LENGTH = 0.0022  # ipad
        # SQUARE_LENGTH = 0.00372  # a3
        BOARD_CORNERS_SHAPE = (H, W)  # Number of X, Y corners,
        if len(glob(os.path.join(frame_folder, "*.npz"))) == 0:
            calibrate_camera_by_chessboard(
                np_imgs, BOARD_CORNERS_SHAPE, SQUARE_LENGTH, frame_folder
            )
    else:
        print("error. mode must be 1 or 0.")


if __name__ == "__main__":
    main()
