'''
Author: sqf
Date: 2024-06-04 15:41:12
LastEditors: Qifan Sun qifsun@tesla.com
LastEditTime: 2024-06-06 00:47:49
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


def generate_aruco(aruco_dict, marker_size, num_markers):
    # 设置 ArUco 字典，这里使用4x4的字典
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict)

    # 计算生成的图像的大小，假设每行放置5个 marker
    markers_per_row = 5
    marker_spacing = 30
    rows = (num_markers + markers_per_row - 1) // markers_per_row  # 向上取整计算行数
    image_width = markers_per_row * (marker_size +
                                     marker_spacing) - marker_spacing
    image_height = rows * (marker_size + marker_spacing) - marker_spacing

    # 创建一个大的空白图像
    full_image = np.ones(
        (image_height, image_width), dtype=np.uint8) * 255  # 白色背景

    # 生成并保存多个 ArUco markers
    for marker_id in range(num_markers):  # 这里生成前10个 markers

        marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)
        marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id,
                                                     marker_size, marker_image,
                                                     1)

        # 计算 marker 在大图像中的位置
        row = marker_id // markers_per_row
        col = marker_id % markers_per_row
        start_y = row * (marker_size + marker_spacing)
        start_x = col * (marker_size + marker_spacing)

        # 将生成的 marker 图像粘贴到大图像上
        full_image[start_y:start_y + marker_size,
                   start_x:start_x + marker_size] = marker_image

    # 添加白色边框
    full_image = cv2.copyMakeBorder(full_image,
                                    marker_spacing,
                                    marker_spacing,
                                    marker_spacing,
                                    marker_spacing,
                                    cv2.BORDER_CONSTANT,
                                    value=255)

    # 显示生成的图像
    cv2.imshow('ArUco Markers', full_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return full_image


def main():
    output_folder = "/Users/qifsun/Desktop/cv89_bmp_bolt_tightening/FV-PROJECTS/fv-bmp-bolt-tightening/data"
    os.makedirs(output_folder, exist_ok=True)

    mode = 2  # 0: charuco; 1: chessboard; 2: aruco markers
    square_size = 400
    border_size = 100

    if mode == 0:
        H = 9
        W = 14
        image_path = os.path.join(output_folder, f'charuco_HxW_{H}x{W}.png')
        img, _, _ = generate_charuco(H, W, border_size, square_size)
    elif mode == 1:
        H = 7
        W = 10
        img = generate_chessboard(H, W, border_size, square_size)
        image_path = os.path.join(output_folder, f'chessboard_HxW_{H}x{W}.png')
    elif mode == 2:
        # generate 4x4 aruco
        aruco_dict = cv2.aruco.DICT_4X4_50
        marker_size = 200
        num_markers = 35
        img = generate_aruco(aruco_dict, marker_size, num_markers)
        image_path = os.path.join(
            output_folder, f'aruco_markers_{marker_size}x{num_markers}.png')

    cv2.imwrite(image_path, img)


if __name__ == "__main__":
    main()
