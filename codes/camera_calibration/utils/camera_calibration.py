'''
Author: sqf
Date: 2024-06-05 10:34:44
LastEditors: Qifan Sun qifsun@tesla.com
LastEditTime: 2024-06-05 22:54:43
FilePath: /FV-PROJECTS/fv-bmp-bolt-tightening/camera_calibration/utils/camera_calibration.py
Description: Some tools for the camera calibration

Copyright (c) 2024 by sqf, All Rights Reserved. 
'''

import os
import cv2
import time
import numpy as np

from glob import glob
from tqdm import tqdm


def drawDetectedCornersCharuco_own(img, corners, ids):
    """
    Draw rectangles and IDs to the corners
    """
    rect_size = 5
    id_font = cv2.FONT_HERSHEY_SIMPLEX
    id_scale = 0.5
    id_color = (255, 255, 0)
    rect_thickness = 1

    # Draw rectangels and IDs
    for (corner, id) in zip(corners, ids):
        corner_x = int(corner[0][0])
        corner_y = int(corner[0][1])
        id_text = "Id: {}".format(str(id[0]))
        id_coord = (corner_x + 2 * rect_size, corner_y + 2 * rect_size)
        cv2.rectangle(img, (corner_x - rect_size, corner_y - rect_size),
                      (corner_x + rect_size, corner_y + rect_size),
                      id_color,
                      thickness=rect_thickness)
        cv2.putText(img, id_text, id_coord, id_font, id_scale, id_color)


def load_img(path):
    """加载图片

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    imgs = glob(os.path.join(path, '*.jpg'))
    # np_imgs = [np.rot90(cv2.imread(x), 3) for x in imgs]
    np_imgs = [cv2.flip(cv2.imread(x), 1) for x in imgs]
    print(f"img shape: {np_imgs[0].shape}")
    return np_imgs, imgs


def load_calib(path):
    """调用路径下最新保存的畸变系数数据

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    np_calib = glob(os.path.join(path, '*.npz'))
    if len(np_calib) != 0:
        newest_calib = sorted(np_calib, reverse=True)[0]

    print(f"using calibrate file: {newest_calib}")

    np_calib = np.load(newest_calib)

    retval, camera_matrix, dist_coeff, rvecs, tvecs = np_calib[
        'retval'], np_calib['camera_matrix'], np_calib['dist_coeff'], np_calib[
            'rvecs'], np_calib['tvecs']

    print(f"retval: {retval}")

    return retval, camera_matrix, dist_coeff, rvecs, tvecs


def create_board(marker_dict,
                 board_corners_shape,
                 square_length,
                 marker_length,
                 size=0):

    if size == 0:
        # Define QR indices up to 50 in dictionary
        dictionary = cv2.aruco.getPredefinedDictionary(marker_dict)
        board = cv2.aruco.CharucoBoard(board_corners_shape,
                                       square_length,
                                       marker_length,
                                       dictionary=dictionary)
        # board_squares_x = board_corners_shape[0] + 1
        # board_squares_y = board_corners_shape[1] + 1
        # board = cv2.aruco.CharucoBoard((board_squares_x, board_squares_y),
        #                                square_length, marker_length,
        #                                dictionary)
    # else:
    #     dictionary = cv2.aruco.getPredefinedDictionary(MARKER_DICT_Dia)
    #     board_squares_x = BOARD_CORNERS_SHAPE_MULTI[0] + 1
    #     board_squares_y = BOARD_CORNERS_SHAPE_MULTI[1] + 1
    #     board = cv2.aruco.CharucoBoard_create(board_squares_x, board_squares_y,
    #                                           SQUARE_LENGHT_MULTI, MARKER_LENGTH_MULTI,
    #                                           dictionary)
    return dictionary, board


def find_chessboard(frame, marker_dict, board_corners_shape, square_length,
                    marker_length):
    """
    Charuco base pose estimation.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect corners first
    # marker_corners - vector of detected marker corners.
    # marker_corners, marker_ids, _ = cv2.aruco.ArucoDetector.detectMarkers(
    #     frame)
    _, board = create_board(marker_dict, board_corners_shape, square_length,
                            marker_length)

    detector = cv2.aruco.CharucoDetector(board)
    qr_corners, qr_ids, marker_corners, marker_ids = detector.detectBoard(gray)

    imsize = gray.shape

    return marker_corners, marker_ids, qr_corners, qr_ids, imsize, board


def calibrate_camera_by_charuco(np_imgs, marker_dict, board_corners_shape,
                                square_length, marker_length, output_result):
    all_corners = []
    all_ids = []

    for frame in tqdm(np_imgs):
        marker_corners, marker_ids, qr_corners, qr_ids, imsize, board = find_chessboard(
            frame, marker_dict, board_corners_shape, square_length,
            marker_length)

        # Any marker is detected
        if marker_ids is not None:
            img_copy = frame.copy()

            # If any corner is detected, draw corner
            if qr_ids is not None:
                drawDetectedCornersCharuco_own(img_copy, qr_corners, qr_ids)
            # Draw markers
            cv2.aruco.drawDetectedMarkers(img_copy, marker_corners, marker_ids)

        # 任何角点被检测到且数量足够
        if qr_corners is not None and qr_ids is not None and len(
                qr_corners) > 4 and len(qr_ids) >= 4:
            all_corners.append(qr_corners)
            all_ids.append(qr_ids)

    # 初始化相机矩阵和畸变系数
    camera_matrix = np.eye(3, dtype=np.float32)
    dist_coeff = np.zeros((5, ), dtype=np.float32)

    retval, camera_matrix, dist_coeff, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_corners, all_ids, board, imsize, camera_matrix, dist_coeff)

    cur_date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    np.savez(os.path.join(output_result, f'{cur_date}_calib.npz'),
             retval=retval,
             camera_matrix=camera_matrix,
             dist_coeff=dist_coeff,
             rvecs=rvecs,
             tvecs=tvecs)

    print('> retval')
    print(retval)
    print('> Camera matrix')
    print(camera_matrix)
    print('> Distortion coefficients')
    print(dist_coeff)


def calibrate_camera_by_chessboard(np_imgs, chessboard_size, square_length,
                                   output_result):
    # 设置世界坐标系中的棋盘格角点
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0],
                           0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_length

    # 准备存储所有图像的对象点和图像点
    objpoints = []  # 3d 点
    imgpoints = []  # 2d 点

    # 逐张图像处理
    for frame in tqdm(np_imgs):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 寻找棋盘格角点
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # 如果找到角点，添加对象点和图像点
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

    # 进行相机校准
    ret, camera_matrix, dist_coeff, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    cur_date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    np.savez(os.path.join(output_result, f'{cur_date}_calib.npz'),
             retval=ret,
             camera_matrix=camera_matrix,
             dist_coeff=dist_coeff,
             rvecs=rvecs,
             tvecs=tvecs)

    print('> retval')
    print(ret)
    print('> Camera matrix')
    print(camera_matrix)
    print('> Distortion coefficients')
    print(dist_coeff)


def main():
    ...


if __name__ == "__main__":
    main()
