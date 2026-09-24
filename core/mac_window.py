# -*- coding: utf-8 -*-
"""
高质感 macOS 风格独立圆角卡片组件 (macOS Sonoma / Sequoia Aesthetic)
特性：
- 【尺寸修长精致】采用 142 x 62 紧凑黄金比例，密集排布更显秀气
- 【真实物理圆角】基于 transparentcolor 抠像技术，消除直角方角与锯齿
- 【整个框体全彩背景】每个框体拥有独一无二、五彩斑斓的鲜活高质感背景色
- 【智能高对比度字体保护】自动计算背景明度，动态匹配深墨黑/纯白字色，100% 清晰绝不看不清
"""

import colorsys
import ctypes
import tkinter as tk
from typing import Dict, Any, Callable, Optional

# Windows 抠像透明关键色（用于把窗口矩形四角镂空为真实平滑圆角）
TRANS_KEY_COLOR = "#000001"

# Windows DWM API 常量 (用于开启 Windows 11 原生圆角投影)
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWCP_ROUND = 2


def apply_win11_round_corners(hwnd: int):
    """尝试给窗口启用 Windows 11 原生系统级圆角和抗锯齿阴影"""
    try:
        dwm = ctypes.windll.dwmapi
        preference = ctypes.c_int(DWMWCP_ROUND)
        dwm.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(preference),
            ctypes.sizeof(preference)
        )
    except Exception:
        pass


def get_unique_mac_theme(index: int) -> Dict[str, str]:
    """
    【独一无二全彩高质感背景与智能对比度配色生成器】
    - 每个框体的背景色完全不同，涵盖粉红、湖蓝、嫩绿、蜜桃、香芋紫、明黄等全彩；
    - 智能判定亮度，自动分配极深石墨黑或高亮纯白文字，确保 100% 极高对比度清晰可读！
    """
    golden_ratio = 0.618033988749895
    hue = (index * golden_ratio) % 1.0

    # 明度交替微调：既有明快马卡龙色，也有高饱和鲜亮糖果色
    lightness = 0.82 if (index % 2 == 0) else 0.88
    saturation = 0.58 if (index % 3 != 0) else 0.45

    # 1. 整个框体的主背景色 (全彩色)
    r1, g1, b1 = colorsys.hls_to_rgb(hue, lightness, saturation)
    bg_hex = '#%02x%02x%02x' % (int(r1 * 255), int(g1 * 255), int(b1 * 255))

    # 2. 标题栏独立底色（在全彩背景基础上微调磨砂感）
    r2, g2, b2 = colorsys.hls_to_rgb(hue, max(0.0, lightness - 0.08), saturation)
    tb_hex = '#%02x%02x%02x' % (int(r2 * 255), int(g2 * 255), int(b2 * 255))

    # 3. 边框与分割线颜色
    r3, g3, b3 = colorsys.hls_to_rgb(hue, max(0.0, lightness - 0.22), min(1.0, saturation + 0.15))
    border_hex = '#%02x%02x%02x' % (int(r3 * 255), int(g3 * 255), int(b3 * 255))

    # 4. 智能对比度算法：计算感知亮度 (Luminance)
    luminance = 0.299 * (r1 * 255) + 0.587 * (g1 * 255) + 0.114 * (b1 * 255)

    if luminance >= 148:
        # 亮色背景 -> 采用高对比度深碳墨黑，锐利清晰绝不发虚
        main_text_color = '#111116'
        sub_title_color = '#383840'
        badge_color = '#C2185B'
    else:
        # 浓色/暗色背景 -> 采用高亮纯白文字
        main_text_color = '#FFFFFF'
        sub_title_color = '#F5F5FA'
        badge_color = '#FFE082'

    return {
        'bg': bg_hex,
        'titlebar_bg': tb_hex,
        'divider': border_hex,
        'border': border_hex,
        'title': sub_title_color,
        'text': main_text_color,
        'sub': badge_color
    }


class MacCardWindow(tk.Toplevel):
    """
    独立高保真 macOS 风格修长圆角小框体窗口
    """
    def __init__(
        self,
        master: tk.Tk,
        x: int,
        y: int,
        width: int,
        height: int,
        theme: Dict[str, str],
        buttons_style: Dict[str, Dict[str, str]],
        message: str,
        tag_text: str = "LoveOS · Memo",
        animate: bool = True,
        slide_offset: int = 14,
        anim_duration_ms: int = 110
    ):
        super().__init__(master)

        self.width = width
        self.height = height
        self.target_x = x
        self.target_y = y
        self.theme = theme
        self.buttons_style = buttons_style
        self.message = message
        self.tag_text = tag_text
        self.slide_offset = slide_offset
        self.anim_duration_ms = anim_duration_ms

        # 1. 移除系统默认厚边框
        self.overrideredirect(True)

        # 2. 启用置顶
        self.attributes("-topmost", True)

        # 3. 启用 Windows 抠像透明色，实现真实平滑圆角边缘
        self.configure(bg=TRANS_KEY_COLOR)
        try:
            self.wm_attributes("-transparentcolor", TRANS_KEY_COLOR)
        except Exception:
            pass

        # 4. 初始位置与透明度
        if animate:
            self.attributes("-alpha", 0.0)
            initial_y = y - slide_offset
            self.geometry(f"{width}x{height}+{x}+{initial_y}")
        else:
            self.geometry(f"{width}x{height}+{x}+{y}")
            self.attributes("-alpha", 0.98)

        # 5. 高精度 Canvas 画布（背景透明）
        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=TRANS_KEY_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # 6. 精美绘制圆角与 Mac 界面元素
        self._render_mac_ui()

        # 7. Windows 11 DWM 系统级圆角兼容
        self.update_idletasks()
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            if not hwnd:
                hwnd = self.winfo_id()
            apply_win11_round_corners(hwnd)
        except Exception:
            pass

        # 8. 启动进入动画
        if animate:
            self.start_enter_animation()

    def _render_mac_ui(self):
        """绘制带真实圆角外边框、全彩背景、双层磨砂标题栏与高对比度文字的卡片"""
        c = self.canvas
        w = self.width
        h = self.height
        radius = 12  # 圆角半径

        titlebar_h = 22
        pad = 2      # 边距留白给圆角描边

        bg_col = self.theme.get('bg', '#FFE6EE')
        tb_col = self.theme.get('titlebar_bg', '#FFD1E0')
        border_col = self.theme.get('border', '#FFA6C2')
        div_col = self.theme.get('divider', '#FFA6C2')

        # 1. 绘制底层完整全彩圆角矩形（主卡片底板，整个框体全彩背景）
        self._draw_smooth_round_rect(
            pad, pad, w - pad, h - pad, radius,
            fill=bg_col, outline=border_col, width=1
        )

        # 2. 绘制顶部标题栏独立区域（带上部圆角）
        self._draw_top_round_rect(
            pad, pad, w - pad, titlebar_h, radius,
            fill=tb_col
        )
        # 标题栏下方 1px 分割线
        c.create_line(pad + 1, titlebar_h, w - pad - 1, titlebar_h, fill=div_col, width=1)

        # 3. macOS 经典高精度交通灯控制三色点（精致小巧）
        dot_r = 3.5
        dot_y = titlebar_h / 2.0
        dot_spacing = 11.0
        start_x = 12.0

        # 关闭红
        btn_close = self.buttons_style.get('close', {'fill': '#FF5F57', 'border': '#E0443E'})
        c.create_oval(
            start_x - dot_r, dot_y - dot_r,
            start_x + dot_r, dot_y + dot_r,
            fill=btn_close['fill'],
            outline=btn_close['border'],
            width=1
        )

        # 最小化黄
        x_yellow = start_x + dot_spacing
        btn_min = self.buttons_style.get('minimize', {'fill': '#FEBC2E', 'border': '#DEA123'})
        c.create_oval(
            x_yellow - dot_r, dot_y - dot_r,
            x_yellow + dot_r, dot_y + dot_r,
            fill=btn_min['fill'],
            outline=btn_min['border'],
            width=1
        )

        # 全屏绿
        x_green = start_x + dot_spacing * 2
        btn_max = self.buttons_style.get('maximize', {'fill': '#28C840', 'border': '#1AAB29'})
        c.create_oval(
            x_green - dot_r, dot_y - dot_r,
            x_green + dot_r, dot_y + dot_r,
            fill=btn_max['fill'],
            outline=btn_max['border'],
            width=1
        )

        # 4. 顶部标题栏微标题（智能高对比度）
        title_color = self.theme.get('title', '#383840')
        c.create_text(
            w // 2 + 12,
            dot_y,
            text=self.tag_text,
            font=("Segoe UI", 7, "bold"),
            fill=title_color,
            anchor="center"
        )

        # 5. 主体告白文案（智能对比度保护：深墨黑或高亮白，高度充裕清晰舒适）
        text_color = self.theme.get('text', '#111116')
        display_msg = self.message

        font_size = 9.0
        if len(display_msg) > 16:
            font_size = 8.0

        content_center_y = titlebar_h + (h - titlebar_h) // 2 - 2
        c.create_text(
            w // 2,
            content_center_y,
            text=display_msg,
            font=("Microsoft YaHei UI", int(font_size), "bold"),
            fill=text_color,
            anchor="center",
            width=w - 14
        )

        # 6. 底部微小装饰角标
        sub_color = self.theme.get('sub', '#C2185B')
        c.create_text(
            w // 2,
            h - 9,
            text="● 100% 心动 · 持续偏爱",
            font=("Segoe UI", 6, "bold"),
            fill=sub_color,
            anchor="center"
        )

    def _draw_smooth_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """绘制平滑四角全圆角矩形"""
        c = self.canvas
        r = radius
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return c.create_polygon(points, smooth=True, **kwargs)

    def _draw_top_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """绘制仅上两角圆角、底部平直的标题栏区域"""
        c = self.canvas
        r = radius
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2,
            x1, y2,
            x1, y1 + r,
            x1, y1
        ]
        return c.create_polygon(points, smooth=True, **kwargs)

    def start_enter_animation(self):
        """进入动画：Ease-Out 柔和物理滑落并平滑淡入"""
        total_frames = 7
        frame_interval_ms = max(12, self.anim_duration_ms // total_frames)

        def _step(frame: int):
            if not self.winfo_exists():
                return

            if frame <= total_frames:
                t = frame / float(total_frames)
                ease = 1.0 - (1.0 - t) ** 2
                cur_y = int(self.target_y - self.slide_offset * (1.0 - ease))
                cur_alpha = min(0.98, ease * 1.05)

                try:
                    self.geometry(f"{self.width}x{self.height}+{self.target_x}+{cur_y}")
                    self.attributes("-alpha", cur_alpha)
                    self.after(frame_interval_ms, _step, frame + 1)
                except Exception:
                    pass
            else:
                try:
                    self.geometry(f"{self.width}x{self.height}+{self.target_x}+{self.target_y}")
                    self.attributes("-alpha", 0.98)
                except Exception:
                    pass

        _step(0)

    def start_exit_animation(self, duration_ms: int = 200, on_complete: Optional[Callable] = None):
        """退场动画：平滑淡出，随后安全销毁窗口"""
        total_frames = 5
        frame_interval_ms = max(15, duration_ms // total_frames)

        def _step(frame: int):
            if not self.winfo_exists():
                if on_complete:
                    on_complete()
                return

            if frame <= total_frames:
                t = frame / float(total_frames)
                cur_alpha = max(0.0, 0.98 * (1.0 - t))
                try:
                    self.attributes("-alpha", cur_alpha)
                    self.after(frame_interval_ms, _step, frame + 1)
                except Exception:
                    self._destroy_self(on_complete)
            else:
                self._destroy_self(on_complete)

        _step(0)

    def _destroy_self(self, on_complete: Optional[Callable] = None):
        """安全自我销毁"""
        try:
            self.destroy()
        except Exception:
            pass
        if on_complete:
            try:
                on_complete()
            except Exception:
                pass
