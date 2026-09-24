# -*- coding: utf-8 -*-
"""
终章全屏烟花与赛博流光字体模块 (Grand Finale) - 纯正横向渐变流动与纯本地离线版
【优化重点】
1. 真实横向流动渐变：字符级高精度排版，色相沿 X 轴水平平滑展开，整行文字呈现与 HTML 预览 100% 一致的横向渐变色彩流动；
2. 零网络依赖与纯离线执行：100% 仅使用本地 Windows API 与 Python 标准库，无任何外部网络请求，拔网线离线秒开；
3. 电影级升腾淡入：第一枚火箭引爆瞬间，中央大字伴随花火从微暗态温润升温并以 Ease-Out 缓动升腾上浮 20px，绝不突兀；
4. 60FPS 极速丝滑流畅：硬上限保护 + 单次批量层级置顶，无任何掉帧卡顿。
"""

import colorsys
import math
import random
import time
import tkinter as tk
import tkinter.font as tkfont
from typing import Callable, Optional

# Windows 硬件透明抠像色（全屏透明穿透，直接悬浮于真实桌面之上）
TRANS_KEY_COLOR = "#000001"

# 高奢珠宝与星河烟花配色库
JEWEL_FIREWORK_COLORS = [
    '#ffd700',  # 璀璨星金
    '#ffe082',  # 柔光香槟金
    '#ff4081',  # 浪漫玫瑰粉
    '#ff1744',  # 炽烈心动绯红
    '#00e5ff',  # 晶莹极光青
    '#7c4dff',  # 梦幻星河紫
    '#ffffff',  # 纯白闪光星辉
    '#ff9100'   # 温暖夕阳金
]


class FireworkParticle:
    """烟花爆炸单颗粒子 (轻量高效物理仿真)"""
    def __init__(self, x: float, y: float, color: str, is_heart: bool = False):
        self.x = x
        self.y = y
        self.color = color
        self.is_heart = is_heart
        self.alpha = 1.0

        if is_heart:
            # 经典心形方程：扩散形成张力十足的立体饱满爱心
            t = random.uniform(0, math.pi * 2)
            r = random.uniform(0.9, 1.85)
            hx = 16 * (math.sin(t) ** 3)
            hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            self.vx = (hx / 16.0) * r * 4.0
            self.vy = (hy / 16.0) * r * 4.0
            self.decay = random.uniform(0.016, 0.024)
            self.size = random.uniform(3.0, 4.8)
            self.gravity = 0.06
            self.friction = 0.965
        else:
            # 璀璨球形牡丹花火
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3.0, 9.8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.decay = random.uniform(0.018, 0.028)
            self.size = random.uniform(2.6, 4.2)
            self.gravity = 0.075
            self.friction = 0.958

    def update(self):
        self.vx *= self.friction
        self.vy *= self.friction
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.alpha -= self.decay

    def is_alive(self):
        return self.alpha > 0


class FireworkRocket:
    """发射上升的烟花火箭 (带发光尾迹线)"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float, is_heart: bool = False):
        self.x = start_x
        self.y = start_y
        self.target_y = target_y
        self.is_heart = is_heart
        speed = random.uniform(15, 20)
        angle = math.atan2(target_y - start_y, target_x - start_x)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = random.choice(JEWEL_FIREWORK_COLORS)
        self.exploded = False

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.vy >= 0 or self.y <= self.target_y:
            self.exploded = True

    def explode(self):
        """爆炸产生高质感适量粒子 (心形 75 颗，球形 55 颗)"""
        particles = []
        count = random.randint(70, 85) if self.is_heart else random.randint(50, 65)
        main_col = self.color

        for _ in range(count):
            # 20% 概率携带星芒白光，其余为烟花主色
            c = '#ffffff' if random.random() < 0.20 else main_col
            particles.append(FireworkParticle(self.x, self.y, c, self.is_heart))
        return particles


class FinaleFireworksWindow(tk.Toplevel):
    """
    终章全屏烟花与赛博流光文字置顶窗口
    【全新升级】
    - 纯正横向水平流动渐变（与 HTML 预览 100% 一致）
    - 零网络请求，纯本地离线运行
    - 电影级淡入与微升腾缓动
    - 60FPS 极速丝滑无卡顿
    """
    def __init__(
        self,
        master: tk.Tk,
        duration_seconds: float = 9.0,
        on_complete: Optional[Callable] = None
    ):
        super().__init__(master)

        self.duration_seconds = duration_seconds
        self.on_complete = on_complete

        # 1. 窗口全屏置顶无边框
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}+0+0")

        # 2. 全屏透明穿透画布
        self.configure(bg=TRANS_KEY_COLOR)
        try:
            self.wm_attributes("-transparentcolor", TRANS_KEY_COLOR)
        except Exception:
            pass

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg=TRANS_KEY_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)

        # 3. 粒子与火箭系统状态
        self.rockets = []
        self.particles = []
        self.is_running = True
        self.rockets_stopped = False
        self.frame_count = 0
        self.flow_phase = 0.0

        # 全局粒子安全上限
        self.MAX_PARTICLES = 360

        # 淡入动效状态
        self.text_fade_done = False
        self.text_fade_step = 0
        self.text_fade_total_steps = 28
        self.prev_lift_offset = 0.0

        # 4. 创建中央横向流动渐变文字图层 (Auth By William)
        self._init_neon_text()

        # 5. 序幕编排：第一发火箭破空而起 ➔ 绽放瞬间文字升腾淡入 ➔ 繁花交错绽放
        self._launch_initial_rocket()
        self.after(280, self._launch_random_rocket)
        # 500ms 时第一朵烟花刚好在空中璀璨绽开，文字伴随火光启动升腾淡入！
        self.after(500, self._start_text_fade_in)
        self.after(680, self._launch_random_rocket)
        self.after(920, self._launch_random_rocket)

        # 6. 启动粒子物理动画主循环 (60 FPS)
        self._animate_loop()

        # 7. 倒计时调度：展示结束前 1.5 秒停止点火自然收尾
        stop_rockets_delay = max(500, int((self.duration_seconds - 1.5) * 1000))
        self.after(stop_rockets_delay, self._stop_new_rockets)
        self.after(int(self.duration_seconds * 1000), self._finish_and_destroy)

    def _get_best_title_font(self):
        """智能选取系统最佳超粗现代字体家族"""
        available = tkfont.families()
        for candidate in ["Segoe UI Black", "Arial Black", "Trebuchet MS", "Segoe UI"]:
            if candidate in available:
                return candidate
        return "Helvetica"

    def _init_neon_text(self):
        """
        初始化中央横向渐变流光文字组件 (Auth By William)
        - 字符级精准对齐与字距排版，实现真实的 X 轴横向彩虹流动渐变
        - 初始坐标微下沉 20px，初始颜色置于不可见透明状态，等待首枚烟花引爆后升腾淡入
        """
        cx = self.width // 2
        cy = self.height // 2

        font_family = self._get_best_title_font()
        title_font = (font_family, 54, "bold")
        font_obj = tkfont.Font(family=font_family, size=54, weight="bold")

        text = "Auth By William"
        total_w = font_obj.measure(text)
        start_x = cx - total_w // 2

        text_tag = "center_text_ui"
        initial_y_offset = 20  # 初始下沉 20px，淡入时平滑上浮

        # 1. 顶部精致小标
        self.subtitle_id = self.canvas.create_text(
            cx, cy - 88 + initial_y_offset,
            text="✦ SPECIAL DEDICATION & PRODUCTION ✦",
            font=("Segoe UI", 12, "bold"),
            fill=TRANS_KEY_COLOR,
            anchor="center",
            tags=text_tag
        )

        # 2. 逐字符创建主字与 Bloom 双层发光晕
        self.char_data_list = []
        for i, ch in enumerate(text):
            if ch == ' ':
                continue
            w_before = font_obj.measure(text[:i])
            w_after = font_obj.measure(text[:i + 1])
            char_cx = start_x + (w_before + w_after) / 2.0
            char_cy = cy + initial_y_offset
            rel_x = (char_cx - start_x) / float(total_w)

            # 外光晕与内微光
            g1 = self.canvas.create_text(
                char_cx + 2.5, char_cy + 2.5,
                text=ch, font=title_font,
                fill=TRANS_KEY_COLOR, anchor="center", tags=text_tag
            )
            g2 = self.canvas.create_text(
                char_cx - 2.5, char_cy - 2.5,
                text=ch, font=title_font,
                fill=TRANS_KEY_COLOR, anchor="center", tags=text_tag
            )

            # 主字符
            mid = self.canvas.create_text(
                char_cx, char_cy,
                text=ch, font=title_font,
                fill=TRANS_KEY_COLOR, anchor="center", tags=text_tag
            )

            self.char_data_list.append({
                'ch': ch,
                'main_id': mid,
                'glow_ids': [g1, g2],
                'rel_x': rel_x
            })

        # 3. 底部深情副标
        self.quote_id = self.canvas.create_text(
            cx, cy + 88 + initial_y_offset,
            text="“ 始于心动 · 终于白首 · 岁岁年年 ”",
            font=("Microsoft YaHei UI", 15, "bold"),
            fill=TRANS_KEY_COLOR,
            anchor="center",
            tags=text_tag
        )

    def _start_text_fade_in(self):
        """启动文字伴随烟花绽放的升腾淡入动效"""
        if not self.is_running:
            return
        self.text_fade_step = 0
        self.prev_lift_offset = 0.0
        self._text_fade_in_step()

    def _text_fade_in_step(self):
        """文字淡入步进算法 (Ease-Out Cubic 平滑升温与上升，淡入阶段即展现横向渐变色)"""
        if not self.is_running or not self.winfo_exists():
            return

        self.text_fade_step += 1
        prog = min(1.0, self.text_fade_step / float(self.text_fade_total_steps))
        # 三次方减速缓动曲线
        ease = 1.0 - math.pow(1.0 - prog, 3)

        # 1. 垂直微升腾上浮位移 (从下沉 20px 平滑上浮至 0px)
        target_lift = 20.0 * ease
        delta_y = -(target_lift - self.prev_lift_offset)
        self.prev_lift_offset = target_lift
        self.canvas.move("center_text_ui", 0, delta_y)

        # 2. 逐字符计算横向渐变色彩与升温
        for item in self.char_data_list:
            rel_x = item['rel_x']
            mid = item['main_id']
            g1, g2 = item['glow_ids']

            # 横向渐变核心公式：色相随相对横向坐标 rel_x 水平展开
            hue = (rel_x * 0.92 + self.flow_phase / (math.pi * 2)) % 1.0
            r, g, b = colorsys.hls_to_rgb(hue, 0.75 * ease, 0.96 * ease)
            main_col = f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'
            self.canvas.itemconfig(mid, fill=main_col)

            # 光晕色彩升温
            h1 = (hue + 0.08) % 1.0
            r1, g1_val, b1 = colorsys.hls_to_rgb(h1, 0.65 * ease, 0.88 * ease)
            self.canvas.itemconfig(g1, fill=f'#{int(r1 * 255):02x}{int(g1_val * 255):02x}{int(b1 * 255):02x}')

            h2 = (hue - 0.08) % 1.0
            r2, g2_val, b2 = colorsys.hls_to_rgb(h2, 0.65 * ease, 0.88 * ease)
            self.canvas.itemconfig(g2, fill=f'#{int(r2 * 255):02x}{int(g2_val * 255):02x}{int(b2 * 255):02x}')

        # 3. 顶部与底部副标渐变显示
        sub_r, sub_g, sub_b = int(255 * ease), int(215 * ease), int(0 * ease)
        self.canvas.itemconfig(self.subtitle_id, fill=f'#{sub_r:02x}{sub_g:02x}{sub_b:02x}')

        q_val = int(255 * ease)
        self.canvas.itemconfig(self.quote_id, fill=f'#{q_val:02x}{q_val:02x}{q_val:02x}')

        # 4. 循环推进或完成
        if prog < 1.0:
            self.after(28, self._text_fade_in_step)
        else:
            self.text_fade_done = True

    def _launch_initial_rocket(self):
        """发射首枚居中引领火箭 (金色彩焰，在中央上空绽放唯美心形)"""
        if not self.is_running:
            return
        tx = int(self.width * 0.50 + random.randint(-40, 40))
        ty = int(self.height * 0.28)
        rocket = FireworkRocket(tx, self.height + 15, tx, ty, is_heart=True)
        self.rockets.append(rocket)

    def _launch_random_rocket(self):
        """发射一颗随机位置与类型的烟花火箭"""
        if not self.is_running or self.rockets_stopped:
            return
        tx = random.randint(int(self.width * 0.15), int(self.width * 0.85))
        ty = random.randint(int(self.height * 0.10), int(self.height * 0.48))
        is_heart = (random.random() > 0.60)
        rocket = FireworkRocket(tx, self.height + 15, tx, ty, is_heart)
        self.rockets.append(rocket)

    def _stop_new_rockets(self):
        """临近结束时停止点火，让天空中已有粒子自然下落燃尽"""
        self.rockets_stopped = True

    def _animate_loop(self):
        """以约 60 FPS 刷新烟花物理动画与横向全彩极光流光文字"""
        if not self.is_running or not self.winfo_exists():
            return

        self.frame_count += 1
        c = self.canvas

        # 1. 优雅稳定的发射节奏：每 16 帧 (约 260ms) 发射 1 发
        if not self.rockets_stopped and self.frame_count % 16 == 0:
            self._launch_random_rocket()

        # 2. 清理上一帧所有的烟花临时图元 (保留中央文字)
        c.delete("firework_entity")

        # 3. 更新并绘制火箭升空轨迹
        active_rockets = []
        for r in self.rockets:
            r.update()
            if r.exploded:
                new_parts = r.explode()
                self.particles.extend(new_parts)
            else:
                c.create_line(
                    r.x, r.y, r.x - r.vx * 1.8, r.y - r.vy * 1.8,
                    fill=r.color, width=2.5,
                    tags="firework_entity"
                )
                active_rockets.append(r)
        self.rockets = active_rockets

        # 4. 更新并绘制烟花火星粒子 (硬上限保护，防止对象失控)
        if len(self.particles) > self.MAX_PARTICLES:
            self.particles = self.particles[-self.MAX_PARTICLES:]

        active_particles = []
        for p in self.particles:
            p.update()
            if p.is_alive():
                sz = p.size
                c.create_oval(
                    p.x - sz, p.y - sz, p.x + sz, p.y + sz,
                    fill=p.color, outline='',
                    tags="firework_entity"
                )
                active_particles.append(p)
        self.particles = active_particles

        # 5. 【核心】更新文字纯正横向水平流动渐变 (Horizontal Gradient Flow)
        if self.text_fade_done:
            # 水平流动相位前进
            self.flow_phase = (self.flow_phase + 0.022) % (math.pi * 2)
            for item in self.char_data_list:
                rel_x = item['rel_x']
                mid = item['main_id']
                g1, g2 = item['glow_ids']

                # 色相随横向 X 轴展开，且随时间向右流动
                hue = (rel_x * 0.92 + self.flow_phase / (math.pi * 2)) % 1.0

                # 主字符高饱和鲜亮色
                r, g, b = colorsys.hls_to_rgb(hue, 0.75, 0.96)
                main_col = f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'
                c.itemconfig(mid, fill=main_col)

                # 伴生 Bloom 光晕动态流动
                h1 = (hue + 0.08) % 1.0
                r1, g1_val, b1 = colorsys.hls_to_rgb(h1, 0.65, 0.88)
                c.itemconfig(g1, fill=f'#{int(r1 * 255):02x}{int(g1_val * 255):02x}{int(b1 * 255):02x}')

                h2 = (hue - 0.08) % 1.0
                r2, g2_val, b2 = colorsys.hls_to_rgb(h2, 0.65, 0.88)
                c.itemconfig(g2, fill=f'#{int(r2 * 255):02x}{int(g2_val * 255):02x}{int(b2 * 255):02x}')

        # 6. 图层层级管理：仅每 12 帧对文字整体打标签进行一次置顶
        if self.frame_count % 12 == 0:
            c.tag_raise("center_text_ui")

        # 保持 60 帧刷新率 (16ms)
        self.after(16, self._animate_loop)

    def _finish_and_destroy(self):
        """彻底销毁全屏透明窗口并触发完成回调"""
        if not self.is_running:
            return
        self.is_running = False

        try:
            self.destroy()
        except Exception:
            pass

        if self.on_complete:
            try:
                self.on_complete()
            except Exception:
                pass
