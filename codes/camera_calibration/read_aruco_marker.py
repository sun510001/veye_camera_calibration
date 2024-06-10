'''
Author: sqf
Date: 2024-06-04 23:41:07
LastEditors: Qifan Sun qifsun@tesla.com
LastEditTime: 2024-06-07 09:58:45
FilePath: /FV-PROJECTS/fv-bmp-bolt-tightening/camera_calibration/read_aruco_marker.py
Description: read aruco markers in the picture(camera matrix needed)

Copyright (c) 2024 by sqf, All Rights Reserved. 
'''

import os
import cv2
from utils.camera_calibration import load_calib

MARKER_LENGTH = 0.011


def draw(frame, intr_matrix, intr_coeffs):
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(
        frame, aruco_dict, parameters=parameters)

    # detector = cv2.aruco.CharucoDetector(board)
    # qr_corners, qr_ids, marker_corners, marker_ids = detector.detectBoard(
    #     frame)

    # 在图片上标出aruco码的位置
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    # 估计出aruco码的位姿，MARKER_LENGTH对应markerLength(二维码的真实大小)参数，单位是meter
    rvecs, tvecs, markerPoints = cv2.aruco.estimatePoseSingleMarkers(
        corners, MARKER_LENGTH, intr_matrix, intr_coeffs)

    if ids is not None:
        for i in range(len(tvecs)):
            # # 根据aruco码的位姿标注出对应的xyz轴, 0.05对应length参数，代表xyz轴画出来的长度
            cv2.drawFrameAxes(frame, intr_matrix, intr_coeffs, rvecs[i],
                              tvecs[i], 0.05)
    return frame


def load_video(video_path, save_folder, intr_matrix, intr_coeffs):
    cap = cv2.VideoCapture(video_path)

    frame_index = 0
    while (cap.isOpened()):
        ret, frame = cap.read()

        # frame = cv2.flip(frame, 1)
        press_key = cv2.waitKey(1) & 0xFF
        if ret == True:
            # save frames
            if save_folder != '':
                image_name = f"image_{frame_index}.jpg"
                cv2.imwrite(os.path.join(save_folder, image_name), frame)
            # draw axis
            frame = draw(frame, intr_matrix, intr_coeffs)
            cv2.imshow("img", frame)
        else:
            break

        frame_index += 1
        if press_key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    video = "/Users/qifsun/Desktop/cv89_bmp_bolt_tightening/FV-PROJECTS/fv-bmp-bolt-tightening/camera_calibration/data/0606_markers/cam1_video_20240607_095753.mp4"
    # image_folder = os.path.join("codes/camera_calibration/data/images", os.path.splitext(os.path.split(video)[1])[0])
    image_folder = ''
    calibration_folder = "/Users/qifsun/Desktop/cv89_bmp_bolt_tightening/FV-PROJECTS/fv-bmp-bolt-tightening/camera_calibration/data/0606_first_capture/cam0_video_20240606_130310"
    # calibration_folder = "/Users/qifsun/Desktop/cv89_bmp_bolt_tightening/FV-PROJECTS/fv-bmp-bolt-tightening/camera_calibration/data/0606_first_capture/cam1_video_20240606_130545"

    retval, camera_matrix, dist_coeff, rvecs, tvecs = load_calib(
        calibration_folder)
    if image_folder != '':
        os.makedirs(image_folder, exist_ok=True)
    intr_matrix, intr_coeffs = camera_matrix, dist_coeff
    load_video(video, image_folder, intr_matrix, intr_coeffs)


if __name__ == "__main__":
    main()
