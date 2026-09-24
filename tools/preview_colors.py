# -*- coding: utf-8 -*-
"""
终章 "Auth By William" 字体颜色多方案交互式预览工坊 (含真实横向渐变流动)
- 运行在真实透明桌面上，伴随 60FPS 极速烟花
- 支持在屏幕上方直接点击按钮或按键盘数字键 [1] [2] [3] [4] [5] 实时无缝切换
- 字符级横向流动渐变，确保与最终成品与 HTML 预览 100% 一模一样！
- 随时按 [ESC] 退出
"""

import colorsys
import math
import random
import time
import tkinter as tk
import tkinter.font as tkfont
from typing import Dict, Any

TRANS_KEY_COLOR = "#000001"

COLOR_SCHEMES: Dict[int, Dict[str, Any]] = {
    1: {
        "title": "方案 1：晶莹星钻金白 (Diamond Ice Gold)",
        "tag": "极度纯净高亮，冰白钻石光泽 + 璀璨淡香槟金流转，清透高贵",
        "subtitle_color": "#FFF1B8",
        "quote_color": "#FFFFFF",
        "mode": "gold_white"
    },
    2: {
        "title": "方案 2：赛博电光青紫 (Cyber Neon Azure & Violet)",
        "tag": "横向渐变：电光湖蓝向极光深紫水平流动，现代科技感与炸裂感",
        "subtitle_color": "#00F2FE",
        "quote_color": "#E0E7FF",
        "mode": "cyber_blue"
    },
    3: {
        "title": "方案 3：落日晚霞珊瑚粉 (Sunset Rose & Coral Glow)",
        "tag": "横向渐变：日落橙金向心动珊瑚粉水平流动，暖调深情，浪漫温柔",
        "subtitle_color": "#FFD8BF",
        "quote_color": "#FFF0F6",
        "mode": "sunset_coral"
    },
    4: {
        "title": "方案 4：极简极客冷月白 (Minimal Pure White Blade)",
        "tag": "100% 极纯高亮白，不带任何杂色，配合冷月柔光，至简至奢华",
        "subtitle_color": "#D9D9D9",
        "quote_color": "#FFFFFF",
        "mode": "pure_white"
    },
    5: {
        "title": "方案 5【已选定成品】：星河全彩极光幻彩 (Cosmic Rainbow Aurora)",
        "tag": "全光谱色相沿 X 轴横向展开流动，青蓝、翡翠绿、金黄、粉紫交织曼舞，生机盎然！",
        "subtitle_color": "#FFD700",
        "quote_color": "#FFFFFF",
        "mode": "rainbow"
    }
}


class FireworkParticle:
    def __init__(self, x: float, y: float, color: str, is_heart: bool = False):
        self.x = x
        self.y = y
        self.color = color
        self.is_heart = is_heart
        self.alpha = 1.0

        if is_heart:
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
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float, is_heart: bool = False):
        self.x = start_x
        self.y = start_y
        self.target_y = target_y
        self.is_heart = is_heart
        speed = random.uniform(15, 20)
        angle = math.atan2(target_y - start_y, target_x - start_x)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = random.choice(['#ffd700', '#ffe082', '#ff4081', '#00e5ff', '#ffffff'])
        self.exploded = False

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.vy >= 0 or self.y <= self.target_y:
            self.exploded = True

    def explode(self):
        particles = []
        count = random.randint(70, 85) if self.is_heart else random.randint(50, 65)
        for _ in range(count):
            c = '#ffffff' if random.random() < 0.20 else self.color
            particles.append(FireworkParticle(self.x, self.y, c, self.is_heart))
        return particles


class ColorPreviewApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_w}x{self.screen_h}+0+0")

        self.root.configure(bg=TRANS_KEY_COLOR)
        try:
            self.root.wm_attributes("-transparentcolor", TRANS_KEY_COLOR)
        except Exception:
            pass

        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_w,
            height=self.screen_h,
            bg=TRANS_KEY_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)

        self.current_scheme_id = 5  # 默认展示选定的方案 5
        self.rockets = []
        self.particles = []
        self.frame_count = 0
        self.flow_phase = 0.0

        available = tkfont.families()
        self.title_font_name = "Segoe UI Black" if "Segoe UI Black" in available else "Arial Black"

        self._init_ui_controls()
        self._init_center_text()
        self.apply_scheme(5)

        self.root.bind_all("<Escape>", lambda e: self.root.destroy())
        for key in ["1", "2", "3", "4", "5"]:
            self.root.bind_all(key, lambda e, k=key: self.apply_scheme(int(k)))

        self._launch_random_rocket()
        self._animate_loop()

    def _init_ui_controls(self):
        cx = self.screen_w // 2
        top_bar_w = 820
        top_bar_h = 78
        bx1 = cx - top_bar_w // 2
        by1 = 20
        bx2 = cx + top_bar_w // 2
        by2 = by1 + top_bar_h

        self.canvas.create_rectangle(
            bx1, by1, bx2, by2,
            fill="#12131C", outline="#2E3048", width=1.5
        )

        self.banner_title_id = self.canvas.create_text(
            cx, by1 + 18,
            text="✨ Auth By William 真实横向流动渐变配色方案切换工坊 (点击或按数字键 1-5，ESC 退出)",
            font=("Microsoft YaHei UI", 10, "bold"),
            fill="#E2E8F0"
        )

        btn_w = 150
        btn_h = 28
        btn_spacing = 8
        total_w = 5 * btn_w + 4 * btn_spacing
        start_x = cx - total_w // 2 + btn_w // 2
        btn_y = by1 + 50

        self.btn_rects = {}
        self.btn_texts = {}

        labels = [
            "1. 晶莹星钻金白",
            "2. 赛博电光青紫",
            "3. 落日晚霞珊瑚",
            "4. 极简冷月纯白",
            "5. 星河极光幻彩 (成品)"
        ]

        for i in range(1, 6):
            x = start_x + (i - 1) * (btn_w + btn_spacing)
            rect_id = self.canvas.create_rectangle(
                x - btn_w // 2, btn_y - btn_h // 2,
                x + btn_w // 2, btn_y + btn_h // 2,
                fill="#1E2030", outline="#3B3E5B", width=1
            )
            text_id = self.canvas.create_text(
                x, btn_y,
                text=labels[i - 1],
                font=("Microsoft YaHei UI", 9, "bold"),
                fill="#94A3B8"
            )
            self.btn_rects[i] = rect_id
            self.btn_texts[i] = text_id

            def _make_handler(scheme_idx):
                return lambda e: self.apply_scheme(scheme_idx)

            self.canvas.tag_bind(rect_id, "<Button-1>", _make_handler(i))
            self.canvas.tag_bind(text_id, "<Button-1>", _make_handler(i))

        self.scheme_desc_id = self.canvas.create_text(
            cx, by2 + 24,
            text="",
            font=("Microsoft YaHei UI", 11, "bold"),
            fill="#FACC15"
        )

    def _init_center_text(self):
        cx = self.screen_w // 2
        cy = self.screen_h // 2 + 10
        title_font = (self.title_font_name, 54, "bold")
        font_obj = tkfont.Font(family=self.title_font_name, size=54, weight="bold")
        text_tag = "center_text_ui"

        # 顶部小标
        self.subtitle_id = self.canvas.create_text(
            cx, cy - 90,
            text="✦ SPECIAL DEDICATION & PRODUCTION ✦",
            font=("Segoe UI", 12, "bold"),
            fill="#FFF1B8",
            anchor="center",
            tags=text_tag
        )

        text = "Auth By William"
        total_w = font_obj.measure(text)
        start_x = cx - total_w // 2

        self.char_data_list = []
        for i, ch in enumerate(text):
            if ch == ' ':
                continue
            w_before = font_obj.measure(text[:i])
            w_after = font_obj.measure(text[:i + 1])
            char_cx = start_x + (w_before + w_after) / 2.0
            char_cy = cy
            rel_x = (char_cx - start_x) / float(total_w)

            # 光晕与主字符
            g1 = self.canvas.create_text(
                char_cx + 2.5, char_cy + 2.5,
                text=ch, font=title_font,
                fill="#000000", anchor="center", tags=text_tag
            )
            g2 = self.canvas.create_text(
                char_cx - 2.5, char_cy - 2.5,
                text=ch, font=title_font,
                fill="#000000", anchor="center", tags=text_tag
            )
            mid = self.canvas.create_text(
                char_cx, char_cy,
                text=ch, font=title_font,
                fill="#FFFFFF", anchor="center", tags=text_tag
            )
            self.char_data_list.append({
                'ch': ch,
                'main_id': mid,
                'glow_ids': [g1, g2],
                'rel_x': rel_x
            })

        # 底部副标
        self.quote_id = self.canvas.create_text(
            cx, cy + 90,
            text="“ 始于心动 · 终于白首 · 岁岁年年 ”",
            font=("Microsoft YaHei UI", 15, "bold"),
            fill="#FFFFFF",
            anchor="center",
            tags=text_tag
        )

    def apply_scheme(self, scheme_id: int):
        if scheme_id not in COLOR_SCHEMES:
            return
        self.current_scheme_id = scheme_id
        sch = COLOR_SCHEMES[scheme_id]

        for i in range(1, 6):
            if i == scheme_id:
                self.canvas.itemconfig(self.btn_rects[i], fill="#2563EB", outline="#60A5FA")
                self.canvas.itemconfig(self.btn_texts[i], fill="#FFFFFF")
            else:
                self.canvas.itemconfig(self.btn_rects[i], fill="#1E2030", outline="#3B3E5B")
                self.canvas.itemconfig(self.btn_texts[i], fill="#94A3B8")

        desc_text = f"【当前生效】{sch['title']} —— {sch['tag']}"
        self.canvas.itemconfig(self.scheme_desc_id, text=desc_text)
        self.canvas.itemconfig(self.subtitle_id, fill=sch['subtitle_color'])
        self.canvas.itemconfig(self.quote_id, fill=sch['quote_color'])

    def _launch_random_rocket(self):
        tx = random.randint(int(self.screen_w * 0.15), int(self.screen_w * 0.85))
        ty = random.randint(int(self.screen_h * 0.10), int(self.screen_h * 0.48))
        is_heart = (random.random() > 0.50)
        rocket = FireworkRocket(tx, self.screen_h + 15, tx, ty, is_heart)
        self.rockets.append(rocket)

    def _animate_loop(self):
        self.frame_count += 1
        c = self.canvas

        if self.frame_count % 18 == 0:
            self._launch_random_rocket()

        c.delete("firework_entity")

        active_rockets = []
        for r in self.rockets:
            r.update()
            if r.exploded:
                self.particles.extend(r.explode())
            else:
                c.create_line(
                    r.x, r.y, r.x - r.vx * 1.8, r.y - r.vy * 1.8,
                    fill=r.color, width=2.5, tags="firework_entity"
                )
                active_rockets.append(r)
        self.rockets = active_rockets

        if len(self.particles) > 350:
            self.particles = self.particles[-350:]

        active_particles = []
        for p in self.particles:
            p.update()
            if p.is_alive():
                sz = p.size
                c.create_oval(
                    p.x - sz, p.y - sz, p.x + sz, p.y + sz,
                    fill=p.color, outline='', tags="firework_entity"
                )
                active_particles.append(p)
        self.particles = active_particles

        # 更新字符级横向渐变色彩
        self.flow_phase = (self.flow_phase + 0.024) % (math.pi * 2)
        mode = COLOR_SCHEMES[self.current_scheme_id]["mode"]

        for item in self.char_data_list:
            rel_x = item['rel_x']
            mid = item['main_id']
            g1, g2 = item['glow_ids']

            if mode == "rainbow":
                # 方案 5：星河全彩极光横向流动渐变
                hue = (rel_x * 0.92 + self.flow_phase / (math.pi * 2)) % 1.0
                r, g, b = colorsys.hls_to_rgb(hue, 0.75, 0.96)
                main_col = f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

                h1 = (hue + 0.08) % 1.0
                r1, g1_val, b1 = colorsys.hls_to_rgb(h1, 0.65, 0.88)
                c.itemconfig(g1, fill=f'#{int(r1 * 255):02x}{int(g1_val * 255):02x}{int(b1 * 255):02x}')

                h2 = (hue - 0.08) % 1.0
                r2, g2_val, b2 = colorsys.hls_to_rgb(h2, 0.65, 0.88)
                c.itemconfig(g2, fill=f'#{int(r2 * 255):02x}{int(g2_val * 255):02x}{int(b2 * 255):02x}')

            elif mode == "cyber_blue":
                # 方案 2：横向青蓝到深紫流动渐变
                phase = (rel_x * 1.5 + self.flow_phase / (math.pi * 2)) % 1.0
                t = (math.sin(phase * math.pi * 2) + 1.0) / 2.0
                r = int(0 * (1.0 - t) + 127 * t)
                g = int(242 * (1.0 - t) + 0 * t)
                b = 255
                main_col = f'#{r:02x}{g:02x}{b:02x}'
                c.itemconfig(g1, fill="#00F2FE")
                c.itemconfig(g2, fill="#7F00FF")

            elif mode == "sunset_coral":
                # 方案 3：横向落日橙红到心动珊瑚粉流动渐变
                phase = (rel_x * 1.5 + self.flow_phase / (math.pi * 2)) % 1.0
                t = (math.sin(phase * math.pi * 2) + 1.0) / 2.0
                r = 255
                g = int(122 * (1.0 - t) + 133 * t)
                b = int(69 * (1.0 - t) + 192 * t)
                main_col = f'#{r:02x}{g:02x}{b:02x}'
                c.itemconfig(g1, fill="#FF4D4F")
                c.itemconfig(g2, fill="#FF85C0")

            elif mode == "gold_white":
                # 方案 1：晶莹白金与微淡香槟金
                phase = (rel_x * 1.2 + self.flow_phase / (math.pi * 2)) % 1.0
                t = (math.sin(phase * math.pi * 2) + 1.0) / 2.0
                r = 255
                g = int(255 * (1.0 - t) + 235 * t)
                b = int(255 * (1.0 - t) + 160 * t)
                main_col = f'#{r:02x}{g:02x}{b:02x}'
                c.itemconfig(g1, fill="#FFE58F")
                c.itemconfig(g2, fill="#91D5FF")

            else:
                # 方案 4：极简纯白
                main_col = "#FFFFFF"
                c.itemconfig(g1, fill="#BAE7FF")
                c.itemconfig(g2, fill="#E6F7FF")

            c.itemconfig(mid, fill=main_col)

        if self.frame_count % 12 == 0:
            c.tag_raise("center_text_ui")

        self.root.after(16, self._animate_loop)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ColorPreviewApp()
    app.run()
