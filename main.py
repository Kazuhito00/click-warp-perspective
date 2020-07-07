#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[summary]
  4点をクリックして射影変換を実施する
[description]
  -
"""

import argparse
from collections import deque

import cv2 as cv

from gui.app_gui import AppGui


def get_args():
    """
    [summary]
        引数解析
    Parameters
    ----------
    None
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--device", type=int, help='camera device number', default=0)
    parser.add_argument("--width", help='capture width', type=int, default=640)
    parser.add_argument(
        "--height", help='capture height', type=int, default=480)
    parser.add_argument(
        "--crop_width", help='capture width', type=int, default=224)
    parser.add_argument(
        "--crop_height", help='capture height', type=int, default=224)

    args = parser.parse_args()

    return args


def main():
    """
    [summary]
        main()
    Parameters
    ----------
    None
    """
    # 引数解析 #################################################################
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    crop_width = args.crop_width
    crop_height = args.crop_height

    # GUI準備 #################################################################
    app_gui = AppGui()

    # カメラ準備 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # 認識対象座標 格納用 #######################################################
    MAX_CLICKPOINTS_NUM = 10
    click_points = []
    click_points_index = 1
    for _ in range(MAX_CLICKPOINTS_NUM):
        click_points.append(deque(maxlen=4))

    while True:
        # カメラキャプチャ #####################################################
        ret, frame = cap.read()
        if not ret:
            print('cap.read() error')
        resize_frame = cv.resize(frame, (int(cap_width), int(cap_height)))

        # マウス左クリックでの解析対象箇所指定 ##################################
        click_point = app_gui.get_mouse_l_click_point()
        if click_point is not None:
            click_points[click_points_index].append(click_point)

        # 指定領域抜き出し #####################################################
        extract_images = app_gui.area_extract(
            resize_frame, click_points, width=crop_width, height=crop_height)

        # GUI描画更新 ##########################################################
        app_gui.update(
            resize_frame,
            click_points,
            extract_images,
        )
        app_gui.show()

        # キー入力(ESC:プログラム終了) #########################################
        key = cv.waitKey(1)
        if 48 <= key <= 57:  # 0 ~ 9
            click_points_index = key - 48
        if key == 99:  # C
            if len(click_points[click_points_index]) == 4:
                app_gui.destroy_window_id(click_points_index)
            click_points[click_points_index].clear()
            extract_images[click_points_index] = None
        if key == 27:  # ESC
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
