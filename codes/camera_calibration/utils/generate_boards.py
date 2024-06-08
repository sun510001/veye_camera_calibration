'''
Author: sqf
Date: 2024-06-04 15:41:12
LastEditors: Qifan Sun qifsun@tesla.com
LastEditTime: 2024-06-05 22:00:13
FilePath: /FV-PROJECTS/fv-bmp-bolt-tightening/camera_calibration/utils/generate_boards.py
Description: generate charuco board and chess board for camera calibration

Copyright (c) 2024 by sqf, All Rights Reserved. 
'''

import os
import cv2
import numpy as np


def generate_charuco(h, w, border_size, square_size):
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    board = cv2.aruco.CharucoBoard((h, w), 0.015, 0.011, dictionary=dictionary)
    img = board.generateImage((h * square_size, w * square_size),
                              None,
                              marginSize=border_size,
                              borderBits=1)
    return img, board, dictionary


def generate_chessboard(h, w, border_size, square_size):
    # 创建一个黑白交替的棋盘格
    chessboard = np.zeros((h * square_size, w * square_size), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            if (i + j) % 2 == 0:
                chessboard[i * square_size:(i + 1) * square_size,
                           j * square_size:(j + 1) * square_size] = 255
    # 添加白色边框
    chessboard_with_border = cv2.copyMakeBorder(chessboard,
                                                border_size,
                                                border_size,
                                                border_size,
                                                border_size,
                                                cv2.BORDER_CONSTANT,
                                                value=255)

    return chessboard_with_border


def main():
    output_folder = "/Users/qifsun/Desktop/cv89_bmp_bolt_tightening/FV-PROJECTS/fv-bmp-bolt-tightening/data"
    os.makedirs(output_folder, exist_ok=True)

    mode = 1  # 0: charuco; 1: chessboard
    square_size = 400
    border_size = 100

    if mode == 0:
        H = 9
        W = 14
        image_path = os.path.join(output_folder, f'charuco_HxW_{H}x{W}.png')
        img, _, _ = generate_charuco(H, W, border_size, square_size)
    else:
        H = 7
        W = 10

        img = generate_chessboard(H, W, border_size, square_size)
        image_path = os.path.join(output_folder, f'chessboard_HxW_{H}x{W}.png')

    cv2.imwrite(image_path, img)


if __name__ == "__main__":
    main()
