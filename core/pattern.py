# -*- coding: utf-8 -*-
"""
手写笔画与爱心轨迹生成引擎 (Handwriting Stroke Engine)
支持专属手写顺序：I -> ❤ -> W -> Y -> M，每一步单独呈现
【高密度升级】显著增加笔画采样密度，形成致密丰满的流动长龙效果
"""

import math
from typing import List, Tuple

Point = Tuple[int, int]


def interpolate_segment(p1: Tuple[int, int], p2: Tuple[int, int], steps: int) -> List[Point]:
    """两点间等距平滑插值（模拟手写笔锋滑过）"""
    pts = []
    for i in range(steps):
        t = i / float(steps)
        x = int(p1[0] + (p2[0] - p1[0]) * t)
        y = int(p1[1] + (p2[1] - p1[1]) * t)
        pts.append((x, y))
    return pts


def get_stroke_I(screen_w: int, screen_h: int, card_w: int, card_h: int) -> List[Point]:
    """【手写字母 I】高密度工整衬线笔顺 (共 72 点)"""
    cx = screen_w // 2
    cy = screen_h // 2
    pts = []

    top_w = 130
    top_y = -210
    bottom_y = 210

    # 1. 顶部横杠 (左 -> 右)
    pts.extend(interpolate_segment((cx - top_w, cy + top_y), (cx + top_w, cy + top_y), 18))
    # 2. 中间垂线下拉 (上 -> 下)
    pts.extend(interpolate_segment((cx, cy + top_y), (cx, cy + bottom_y), 36))
    # 3. 底部横杠 (左 -> 右)
    pts.extend(interpolate_segment((cx - top_w, cy + bottom_y), (cx + top_w, cy + bottom_y), 18))

    return [(px - card_w // 2, py - card_h // 2) for px, py in pts]


def get_stroke_HEART(screen_w: int, screen_h: int, card_w: int, card_h: int, count: int = 96) -> List[Point]:
    """【手写爱心 ❤】缓速深情高密度勾勒轨迹 (共 96 点)"""
    cx = screen_w // 2
    cy = screen_h // 2 - 25
    scale = min(screen_w / 44.0, screen_h / 40.0)

    pts = []
    for i in range(count):
        t = (i / float(count)) * 2.0 * math.pi
        x_val = 16 * (math.sin(t) ** 3)
        y_val = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))

        px = int(cx + x_val * scale - card_w // 2)
        py = int(cy + y_val * scale - card_h // 2)

        px = max(10, min(screen_w - card_w - 10, px))
        py = max(10, min(screen_h - card_h - 10, py))
        pts.append((px, py))

    return pts


def get_stroke_W(screen_w: int, screen_h: int, card_w: int, card_h: int) -> List[Point]:
    """【手写字母 W】高密度连贯四折笔画 (共 92 点)"""
    cx = screen_w // 2
    cy = screen_h // 2
    pts = []

    p0 = (cx - 215, cy - 185)  # 左上
    p1 = (cx - 108, cy + 190)  # 谷底 1
    p2 = (cx,       cy - 50)   # 中峰
    p3 = (cx + 108, cy + 190)  # 谷底 2
    p4 = (cx + 215, cy - 185)  # 右上

    pts.extend(interpolate_segment(p0, p1, 23))
    pts.extend(interpolate_segment(p1, p2, 23))
    pts.extend(interpolate_segment(p2, p3, 23))
    pts.extend(interpolate_segment(p3, p4, 23))

    return [(px - card_w // 2, py - card_h // 2) for px, py in pts]


def get_stroke_Y(screen_w: int, screen_h: int, card_w: int, card_h: int) -> List[Point]:
    """【手写字母 Y】高密度经典手写笔顺 (共 74 点)"""
    cx = screen_w // 2
    cy = screen_h // 2
    pts = []

    top_y = -195
    center_y = -10
    bottom_y = 205

    p_left  = (cx - 170, cy + top_y)
    p_right = (cx + 170, cy + top_y)
    p_mid   = (cx,       cy + center_y)
    p_bot   = (cx,       cy + bottom_y)

    pts.extend(interpolate_segment(p_left, p_mid, 22))
    pts.extend(interpolate_segment(p_right, p_mid, 22))
    pts.extend(interpolate_segment(p_mid, p_bot, 30))

    return [(px - card_w // 2, py - card_h // 2) for px, py in pts]


def get_stroke_M(screen_w: int, screen_h: int, card_w: int, card_h: int) -> List[Point]:
    """【手写字母 M】高密度连笔挺拔笔顺 (共 92 点)"""
    cx = screen_w // 2
    cy = screen_h // 2
    pts = []

    p0 = (cx - 215, cy + 195)  # 左下
    p1 = (cx - 215, cy - 185)  # 左竖峰
    p2 = (cx,       cy + 55)   # 中心低谷
    p3 = (cx + 215, cy - 185)  # 右竖峰
    p4 = (cx + 215, cy + 195)  # 右下

    pts.extend(interpolate_segment(p0, p1, 23))
    pts.extend(interpolate_segment(p1, p2, 23))
    pts.extend(interpolate_segment(p2, p3, 23))
    pts.extend(interpolate_segment(p3, p4, 23))

    return [(px - card_w // 2, py - card_h // 2) for px, py in pts]
