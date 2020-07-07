#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import numpy as np
import cv2 as cv


class AppGui:
    """
    [summary]
    アプリケーションウィンドウクラス
    [description]
    -
    """
    _window_position = [0, 0]
    _window_name = ''
    _frame = None
    _extract_images = None

    _click_point = None

    def __init__(self, window_name='DEBUG', window_position=None):
        self._window_name = window_name
        self._window_position = window_position

        cv.namedWindow(self._window_name)
        cv.setMouseCallback(self._window_name, self._mouse_callback)

    def update(self, frame, click_points, extract_images):
        """
        [summary]
          描画内容更新
        """
        self._frame = copy.deepcopy(frame)
        self._extract_images = copy.deepcopy(extract_images)

        # 選択箇所描画
        self._frame = self._draw_click_points(self._frame, click_points)

    def show(self):
        """
        [summary]
          描画
        """
        cv.imshow(self._window_name, self._frame)
        if self._window_position is not None:
            cv.moveWindow(self._window_name, self._window_position[0],
                          self._window_position[1])

        for id, extract_image in enumerate(self._extract_images):
            if extract_image is None:
                continue
            cv.imshow('ID:' + str(id), extract_image)

    def get_mouse_l_click_point(self):
        """
        [summary]
          マウス左クリック座標を取得
        """
        click_point = None
        if self._click_point is not None:
            click_point = self._click_point
            self._click_point = None

        return click_point

    def area_extract(self, image, area_points_list, width=224, height=224):
        """
        [summary]
          指定座標を元に射影変換した画像を取得
        """
        extract_images = []

        for _, area_points in enumerate(area_points_list):
            if len(area_points) < 4:
                extract_images.append(None)
            elif len(area_points) == 4:
                temp_image = copy.deepcopy(image)

                point1 = area_points[0]
                point2 = area_points[1]
                point3 = area_points[2]
                point4 = area_points[3]

                # 射影変換
                pts1 = np.float32([
                    point1,
                    point2,
                    point3,
                    point4,
                ])
                pts2 = np.float32([
                    [0, 0],
                    [width, 0],
                    [width, height],
                    [0, height],
                ])
                M = cv.getPerspectiveTransform(pts1, pts2)
                extract_images.append(
                    cv.warpPerspective(temp_image, M, (width, height)))

        return extract_images

    def destroy_window_id(self, id):
        """
        [summary]
          指定IDのウィンドウを削除する
        """
        cv.destroyWindow('ID:' + str(id))

    def _draw_click_points(self, frame, points):
        """
        [summary]
          クリック座標描画
        """
        for id, temp_points in enumerate(points):
            # 左上座標を取得
            if len(temp_points) > 0:
                point1 = temp_points[0]
                center = (np.average(np.array(temp_points)[:, 0]),
                          np.average(np.array(temp_points)[:, 1]))
                for point in temp_points:
                    if point[1] < center[1]:
                        if point[0] < center[0]:
                            point1 = point

            # 各ポイントをつないだ線を描画
            if len(temp_points) >= 3:
                frame = cv.drawContours(frame, [np.array(temp_points)], -1,
                                        (255, 255, 255), 3)
                frame = cv.drawContours(frame, [np.array(temp_points)], -1,
                                        (0, 0, 0), 2)

            # ID情報と各点を描画
            for index, point in enumerate(temp_points):
                if index == 0:
                    cv.rectangle(frame, (point1[0], point1[1] - 25),
                                 (point1[0] + 35, point1[1] - 8), (0, 0, 0),
                                 -1)
                    cv.putText(frame, 'ID:' + str(id),
                               (point1[0], point1[1] - 10),
                               cv.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 1,
                               cv.LINE_AA)
                frame = cv.circle(frame, (point[0], point[1]), 5,
                                  (255, 255, 255), -1)
                frame = cv.circle(frame, (point[0], point[1]), 4, (0, 0, 0),
                                  -1)
        return frame

    def _mouse_callback(self, event, x, y, flags, param):
        """
        [summary]
          マウスコールバック
        """
        if event == cv.EVENT_LBUTTONDOWN:
            self._click_point = [x, y]
