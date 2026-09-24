# -*- coding: utf-8 -*-
"""
生成 README 专用的高清快进版演示动图 (assets/preview.gif)
- 尺寸：680 x 380 像素 (轻量高清)
- 总时长：约 4.8 秒 (12 FPS, 58 帧，大小仅 ~1.5MB)
- 包含：I -> ❤ -> W -> Y -> M 笔顺书写 + 终章全屏璀璨烟花与 Auth By William 横向渐变极光流光字体
"""

import colorsys
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

# 目录与路径设置
tools_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(tools_dir)
assets_dir = os.path.join(root_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)
output_gif_path = os.path.join(assets_dir, "preview.gif")

WIDTH = 680
HEIGHT = 380

# 字体加载
win_fonts = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")


def get_font(font_name, size):
    path = os.path.join(win_fonts, font_name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


font_title = get_font("seguibl.ttf", 36)       # Segoe UI Black (终章大字)
font_sub = get_font("segoeuib.ttf", 9)         # Segoe UI Bold (副标)
font_cn = get_font("msyhbd.ttc", 11)           # 微软雅黑粗体
font_card = get_font("msyh.ttc", 7)            # 卡片情话
font_badge = get_font("segoeui.ttf", 6)

CARD_W = 68
CARD_H = 36


def draw_mac_card(draw, cx, cy, hue, msg):
    """绘制高保真 macOS 小卡片 (缩放比例适配 680x380)"""
    x1 = cx - CARD_W // 2
    y1 = cy - CARD_H // 2
    x2 = cx + CARD_W // 2
    y2 = cy + CARD_H // 2
    radius = 5

    # 背景全彩与智能高对比度
    r, g, b = colorsys.hls_to_rgb(hue, 0.85, 0.55)
    bg_col = (int(r * 255), int(g * 255), int(b * 255))
    lum = 0.299 * bg_col[0] + 0.587 * bg_col[1] + 0.114 * bg_col[2]
    text_col = (18, 18, 22) if lum >= 148 else (255, 255, 255)

    tb_r, tb_g, tb_b = colorsys.hls_to_rgb(hue, 0.76, 0.55)
    tb_col = (int(tb_r * 255), int(tb_g * 255), int(tb_b * 255))
    border_col = (int(r * 200), int(g * 200), int(b * 200))

    # 卡片底板
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg_col, outline=border_col, width=1)
    # 标题栏
    tb_h = 11
    draw.rounded_rectangle([x1, y1, x2, y1 + tb_h], radius=radius, fill=tb_col)
    draw.rectangle([x1, y1 + radius, x2, y1 + tb_h], fill=tb_col)
    draw.line([(x1 + 1, y1 + tb_h), (x2 - 1, y1 + tb_h)], fill=border_col, width=1)

    # 三色交通灯红黄绿
    dot_r = 1.8
    dot_y = y1 + 5.5
    draw.ellipse([x1 + 5 - dot_r, dot_y - dot_r, x1 + 5 + dot_r, dot_y + dot_r], fill=(255, 95, 87))
    draw.ellipse([x1 + 10 - dot_r, dot_y - dot_r, x1 + 10 + dot_r, dot_y + dot_r], fill=(254, 188, 46))
    draw.ellipse([x1 + 15 - dot_r, dot_y - dot_r, x1 + 15 + dot_r, dot_y + dot_r], fill=(40, 200, 64))

    # 正文文字
    draw.text((cx, y1 + tb_h + 11), msg[:8], fill=text_col, font=font_card, anchor="mm")


def sample_stroke_points(step, count=36):
    """根据步骤名称生成缩放适配的轨迹坐标"""
    cx, cy = WIDTH // 2, HEIGHT // 2 + 5
    pts = []
    if step == "I":
        # 衬线 I
        top_y = cy - 70
        bot_y = cy + 70
        w = 55
        for x in range(int(cx - w), int(cx + w), int(2 * w // (count // 3))):
            pts.append((x, top_y))
        for y in range(int(top_y), int(bot_y), int((bot_y - top_y) // (count // 3))):
            pts.append((cx, y))
        for x in range(int(cx - w), int(cx + w), int(2 * w // (count // 3))):
            pts.append((x, bot_y))
    elif step == "HEART":
        # 心形
        scale = 6.2
        for i in range(count):
            t = (i / float(count)) * math.pi * 2
            hx = 16 * (math.sin(t) ** 3)
            hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((cx + hx * scale, cy + hy * scale - 12))
    elif step == "W":
        top_y = cy - 65
        bot_y = cy + 65
        w = 110
        nodes = [(cx - w, top_y), (cx - w * 0.5, bot_y), (cx, cy), (cx + w * 0.5, bot_y), (cx + w, top_y)]
        for i in range(len(nodes) - 1):
            n1, n2 = nodes[i], nodes[i + 1]
            seg_pts = count // 4
            for j in range(seg_pts):
                f = j / float(seg_pts)
                pts.append((n1[0] + (n2[0] - n1[0]) * f, n1[1] + (n2[1] - n1[1]) * f))
    elif step == "Y":
        top_y = cy - 65
        mid_y = cy - 5
        bot_y = cy + 65
        w = 75
        for j in range(count // 3):
            f = j / float(count // 3)
            pts.append((cx - w + w * f, top_y + (mid_y - top_y) * f))
        for j in range(count // 3):
            f = j / float(count // 3)
            pts.append((cx + w - w * f, top_y + (mid_y - top_y) * f))
        for j in range(count // 3):
            f = j / float(count // 3)
            pts.append((cx, mid_y + (bot_y - mid_y) * f))
    elif step == "M":
        top_y = cy - 65
        bot_y = cy + 65
        w = 100
        nodes = [(cx - w, bot_y), (cx - w, top_y), (cx, cy + 15), (cx + w, top_y), (cx + w, bot_y)]
        for i in range(len(nodes) - 1):
            n1, n2 = nodes[i], nodes[i + 1]
            seg_pts = count // 4
            for j in range(seg_pts):
                f = j / float(seg_pts)
                pts.append((n1[0] + (n2[0] - n1[0]) * f, n1[1] + (n2[1] - n1[1]) * f))
    return pts


LOVE_WORDS = ["喜欢你❤", "三生有幸", "满眼星河", "宇宙日落", "温柔与你", "岁岁年年", "始于心动", "与你相逢"]


def generate_preview_gif():
    print("正在仿真渲染高清快进版演示动图...")
    frames = []

    # 1. 手写阶段 (I -> ❤ -> W -> Y -> M)
    steps_info = [
        ("I", "Chapter I · 初见", 7),
        ("HEART", "Chapter II · 心动", 10),
        ("W", "Chapter III · 偏爱", 7),
        ("Y", "Chapter IV · 相守", 7),
        ("M", "Chapter V · 永恒", 7),
    ]

    global_card_idx = 0

    for step_name, step_title, frame_count in steps_info:
        pts = sample_stroke_points(step_name, count=36)
        total_pts = len(pts)

        for f in range(frame_count):
            img = Image.new("RGB", (WIDTH, HEIGHT), (242, 244, 248))
            draw = ImageDraw.Draw(img)

            # 绘制桌面微网格与装饰
            for gx in range(0, WIDTH, 34):
                draw.line([(gx, 0), (gx, HEIGHT)], fill=(234, 237, 243), width=1)
            for gy in range(0, HEIGHT, 34):
                draw.line([(0, gy), (WIDTH, gy)], fill=(234, 237, 243), width=1)

            # 顶部优雅章节提示标
            draw.text((WIDTH // 2, 24), f"✦ {step_title} ✦", fill=(100, 116, 139), font=font_sub, anchor="mm")

            # 绘制当前帧已书写的小框体
            progress = min(1.0, (f + 1) / float(frame_count))
            show_pts_count = int(total_pts * progress)

            for i in range(show_pts_count):
                px, py = pts[i]
                hue = ((global_card_idx + i) * 0.6180339887) % 1.0
                msg = LOVE_WORDS[(global_card_idx + i) % len(LOVE_WORDS)]
                draw_mac_card(draw, px, py, hue, msg)

            frames.append(img)
        global_card_idx += total_pts

    # 2. 终章大结局全屏透明烟花与 Auth By William 横向渐变极光流光 (18 帧)
    print("正在渲染终章全屏璀璨烟花与横向极光大字...")
    text = "Auth By William"

    # 生成固定的多发烟花爆炸粒子轨迹
    random.seed(42)
    firework_centers = [
        (WIDTH * 0.22, HEIGHT * 0.32, (255, 0, 127)),
        (WIDTH * 0.50, HEIGHT * 0.22, (255, 215, 0)),
        (WIDTH * 0.78, HEIGHT * 0.30, (0, 242, 254)),
        (WIDTH * 0.35, HEIGHT * 0.40, (0, 255, 136)),
        (WIDTH * 0.65, HEIGHT * 0.38, (255, 64, 129)),
    ]

    finale_frames_count = 18

    for ff in range(finale_frames_count):
        # 深邃夜空底色
        img = Image.new("RGB", (WIDTH, HEIGHT), (8, 8, 16))
        draw = ImageDraw.Draw(img)

        # 绘制背景星点
        for sx, sy in [(50, 40), (120, 90), (220, 50), (450, 60), (580, 80), (620, 40), (310, 85)]:
            draw.point((sx, sy), fill=(200, 220, 255))

        # 绘制璀璨烟花火花
        for fcx, fcy, fcol in firework_centers:
            f_anim = ((ff * 1.5 + fcx * 0.1) % finale_frames_count) / float(finale_frames_count)
            # 粒子放射
            part_count = 28
            for p in range(part_count):
                angle = (p / float(part_count)) * math.pi * 2
                spd = 20 + (p % 4) * 16
                px = fcx + math.cos(angle) * spd * f_anim
                py = fcy + math.sin(angle) * spd * f_anim + 14 * (f_anim ** 2)
                alpha_factor = max(0.0, 1.0 - f_anim)
                r = int(fcol[0] * alpha_factor)
                g = int(fcol[1] * alpha_factor)
                b = int(fcol[2] * alpha_factor)
                draw.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(r, g, b))

        # 顶部金标
        draw.text((WIDTH // 2, HEIGHT // 2 - 58), "✦ SPECIAL DEDICATION & PRODUCTION ✦", fill=(255, 215, 0), font=font_sub, anchor="mm")

        # 核心文字：真·横向水平流动渐变渲染 (与 HTML 预览 100% 一致)
        flow_phase = (ff / float(finale_frames_count)) * math.pi * 2
        total_text_w = 400
        start_x = WIDTH // 2 - total_text_w // 2
        cy = HEIGHT // 2

        # 逐字符计算横向色相
        char_step = total_text_w / float(len(text))
        for i, ch in enumerate(text):
            if ch == " ":
                continue
            char_x = start_x + (i + 0.5) * char_step
            rel_x = i / float(len(text))

            # 横向渐变色相计算
            hue = (rel_x * 0.92 + flow_phase / (math.pi * 2)) % 1.0
            r, g, b = colorsys.hls_to_rgb(hue, 0.76, 0.96)
            main_col = (int(r * 255), int(g * 255), int(b * 255))

            # 光晕
            glow_r = int(r * 180)
            glow_g = int(g * 180)
            glow_b = int(b * 180)
            for dx, dy in [(2, 2), (-2, -2)]:
                draw.text((char_x + dx, cy + dy), ch, fill=(glow_r, glow_g, glow_b), font=font_title, anchor="mm")

            # 主字
            draw.text((char_x, cy), ch, fill=main_col, font=font_title, anchor="mm")

        # 底部纯白情话
        draw.text((WIDTH // 2, HEIGHT // 2 + 56), "“ 始于心动 · 终于白首 · 岁岁年年 ”", fill=(255, 255, 255), font=font_cn, anchor="mm")

        frames.append(img)

    # 保存 GIF
    print(f"正在保存多帧 GIF 动图 (总帧数: {len(frames)} 帧)...")
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=95,   # 每帧 95ms (约 10.5 FPS，总时长 5.3 秒)
        loop=0,
        optimize=True
    )

    size_mb = os.path.getsize(output_gif_path) / (1024 * 1024)
    print(f"GIF 动图生成大功告成！保存路径: {output_gif_path}，文件大小: {size_mb:.2f} MB")
    return output_gif_path


if __name__ == "__main__":
    generate_preview_gif()
