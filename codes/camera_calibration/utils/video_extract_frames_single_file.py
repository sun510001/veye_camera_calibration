"""
Author: sqf
Date: 2024-06-05 10:53:07
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2024-06-09 15:50:02
FilePath: /veye_camera_calibration/codes/camera_calibration/utils/video_extract_frames_single_file.py
Description: 单视频文件抽帧, 4线程抽帧时间比单线程抽帧减少50%.

Copyright (c) 2024 by sqf, All Rights Reserved. 
"""

import os
import cv2
import tqdm
import argparse
from multiprocessing import Pool


def win_path_replace(path):
    """
    解决windows 下使用os.path.join时路径有双斜杠问题
    :param path: 有问题路径
    :return: 修复后的路径
    """
    return path.replace("\\", "/")


def split_frame_to_list(total_frame, part):
    """将视频的总帧数分割成片段便于多线程

    Args:
        total_frame (int): 视频的总帧数
        part (int): 分为几段

    Returns:
        split_frame_list (list): 帧数片段
    """
    split_list = []
    for x in range(0, total_frame, total_frame // part):
        if x + (total_frame // part) <= total_frame:
            split_list.append([x, x + (total_frame // part) - 1])
        else:
            split_list.append([x, total_frame])
    return split_list


# def check_rotation(path_video_file):
#     """https://stackoverflow.com/questions/53097092/frame-from-video-is-upside-down-after-extracting
#        解决手机视频竖屏拍摄在抽帧的时候变横屏的问题

#     Args:
#         path_video_file (_type_): 视频文件地址

#     Returns:
#         _type_: 需要转动的角度
#     """
#     # this returns meta-data of the video file in form of a dictionary
#     meta_dict = ffmpeg.probe(path_video_file)

#     # from the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
#     # we are looking for
#     rotateCode = None
#     if int(meta_dict['streams'][0]['tags']['rotate']) == 90:
#         rotateCode = cv2.ROTATE_90_CLOCKWISE
#     elif int(meta_dict['streams'][0]['tags']['rotate']) == 180:
#         rotateCode = cv2.ROTATE_180
#     elif int(meta_dict['streams'][0]['tags']['rotate']) == 270:
#         rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE

#     return rotateCode


def frame_extract_by_interval(
    video_path,
    save_path,
    time_set=3,
    start_frame=None,
    end_frame=None,
    frame_list=None,
    rotate_code=None,
    qulity=0,
):
    """
    根据帧数列表提取图片, 所有视频抽的帧放在一起
    :param video_path: 视频的全局路径
    :param save_path: 保存抽帧结果的文件夹
    :param time_set: 设定1秒抽几帧
    :param start_frame: 切片开始帧数
    :param end_frame: 切片结束帧数
    :param frame_list: 如果不为空, 则使用抽帧列表中的帧进行抽帧
    :return:
    """
    if start_frame is None:
        start_frame = 0

    video_name = os.path.splitext(os.path.split(video_path)[1])[0]
    capture = cv2.VideoCapture(video_path)
    total_frame = capture.get(7)  # 获取该视频的总帧数
    fps = capture.get(5)  # 获取视频fps
    interval = fps // time_set

    if end_frame is None:
        end_frame = total_frame

    if frame_list:
        total = len(frame_list)
    else:
        total = int((end_frame - start_frame) // interval)

    with tqdm.tqdm(total=total) as ext_bar:
        for index in range(0, int(total_frame) + 1):
            ret, frame = capture.read()  # frame是BGR格式
            # frame = cv2.flip(frame, 1)
            if rotate_code is not None:  # 如果存在转动信息, 则转动图片
                frame = cv2.rotate(frame, rotate_code)

            if frame is None:
                break
            if not ret:
                print("\nWarning! Loss this frame.\n")

            if (
                frame_list is None
                and start_frame <= index <= end_frame
                and index % interval == 0
            ):
                save_frame = "{}/{}_{:08d}.jpg".format(
                    save_path,
                    video_name,
                    index,
                )
                # cv2.imwrite(save_frame, frame, [
                #             cv2.IMWRITE_PNG_COMPRESSION, qulity])
                cv2.imwrite(save_frame, frame)
                ext_bar.update(1)

            if frame_list is not None and index in frame_list:
                save_frame = "{}/{}_{:08d}.jpg".format(
                    save_path,
                    video_name,
                    index,
                )
                # cv2.imwrite(save_frame, frame, [
                #             cv2.IMWRITE_PNG_COMPRESSION, qulity])
                cv2.imwrite(save_frame, frame)
                ext_bar.update(1)

            if index > end_frame:
                break

            ext_bar.set_description(
                f"Loading the frame number of {os.path.split(video_path)[1]}: {index}"
            )  # 打印抽帧进度
            index += 1

    capture.release()
    print(
        f"\nImages which is extracted from the clip {[start_frame, end_frame]} are saved in {save_path}.\n"
    )


def init_process(g_var1, g_var2, g_var3, g_var4, g_var5):
    """
    全局函数
    :param global_vars:
    :return:
    """
    global video_path, output, time_set, rotateCode, qulity
    video_path, output, time_set, rotateCode, qulity = (
        g_var1,
        g_var2,
        g_var3,
        g_var4,
        g_var5,
    )


def do_extract_frames(frames_list):
    try:
        frame_extract_by_interval(
            video_path,
            output,
            time_set,
            start_frame=frames_list[0],
            end_frame=frames_list[1],
            rotate_code=rotateCode,
        )
    except BaseException as e:
        print(f"\nWarning! Frames: {frames_list} is not video type. Skip.\n")
        print("\nERROR: \n")
        print(e)


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video_path",
        type=str,
        default="/home/sun/Desktop/codes/veye_camera_calibration/codes/camera_calibration/data/video8_capture_2024-06-09_16-41-35.mp4",
        help="存放视频文件的路径",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="/home/sun/Desktop/codes/veye_camera_calibration/codes/camera_calibration/data/video8_capture_2024-06-09_16-41-35",
        help="存放抽帧图片的文件夹路径",
    )
    parser.add_argument("--time_set", type=int, default=1, help="1秒内抽取图片数量")
    parser.add_argument("--proc", type=int, default=4, help="开启线程数")
    parser.add_argument(
        "--qulity", type=int, default=2, help="图片压缩率[0-9], 0为无损"
    )
    return parser.parse_args()


def main():
    args = init_args()
    time_set = args.time_set
    proc = args.proc
    qulity = args.qulity
    video_path = win_path_replace(args.video_path)
    output = win_path_replace(args.output_dir)
    os.makedirs(output, exist_ok=True)
    # rotateCode = check_rotation(video_path)  # 检查视频是否被旋转
    rotateCode = None
    capture = cv2.VideoCapture(video_path)
    total_frame = int(capture.get(7))  # 获取该视频的总帧数
    capture.release()
    split_frame_list = split_frame_to_list(total_frame, proc)

    with Pool(
        processes=proc,
        initializer=init_process,
        initargs=(
            video_path,
            output,
            time_set,
            rotateCode,
            qulity,
        ),
    ) as pool:
        pool.map(do_extract_frames, split_frame_list)


if __name__ == "__main__":
    main()
