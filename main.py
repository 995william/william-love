# -*- coding: utf-8 -*-
"""
多窗口爱心与自定义字母手写表白程序 - 主程序
特性：
1. 专属手写笔顺分步呈现：I -> ❤ -> W -> Y -> M，每一步在屏幕中央单独书写、定格、翻篇；
2. 彻底重构高精度 macOS Sonoma / Sequoia 双层质感卡片（Titlebar 分区、细腻分割线、高保真三色交通灯、石墨黑精致排版）；
3. 心形生成速度舒缓放慢（50ms），呈现出深情书法运笔般的仪式感；
4. 全流程无大底板窗口，通透悬浮于桌面之上；
5. 运行期间锁定并隐藏鼠标，按 ESC 键瞬间安全急停；
6. 纯 Python 原生标准库实现，零第三方依赖，天生为打包单文件 exe 优化。
"""

import argparse
import ctypes
import os
import random
import sys
import threading
import time
import tkinter as tk

# 确保项目根目录在 sys.path 中
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入配置与模块
import config
from core.finale_fireworks import FinaleFireworksWindow
from core.mac_window import MacCardWindow, get_unique_mac_theme
from core.mouse_lock import mouse_controller
from core import pattern


def enable_high_dpi():
    """使程序感知高分屏 DPI，确保窗口清晰与坐标精准"""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class MultiWindowLoveApp:
    def __init__(self, no_mouse_lock: bool = False, speed_multiplier: float = 1.0):
        enable_high_dpi()

        self.disable_mouse = not no_mouse_lock if no_mouse_lock else config.DISABLE_MOUSE_DURING_RUN
        self.speed_multiplier = speed_multiplier

        # 初始化 Tkinter 主控环境并完全隐藏主窗口（绝不显示大窗口）
        self.root = tk.Tk()
        self.root.withdraw()

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.card_w = config.CARD_WIDTH
        self.card_h = config.CARD_HEIGHT

        # 状态控制
        self.steps = list(config.STEPS_SEQUENCE)
        self.current_step_index = 0
        self.current_step_cards = []
        self.all_active_cards = []
        self.scheduled_after_ids = []
        self.is_closing = False
        self.global_msg_index = 0

        # 配置退出机制
        self._setup_exit_handlers()

    def _setup_exit_handlers(self):
        """配置退出热键与安全拦截"""
        if config.ALLOW_ESC_EXIT:
            self.root.bind_all("<Escape>", lambda event: self.close_all(fast=True))
            mouse_controller.set_esc_callback(lambda: self.close_all(fast=True))

    def get_step_points(self, step_name: str):
        """获取当前步骤的坐标轨迹"""
        step = step_name.upper()
        if step == "I":
            return pattern.get_stroke_I(self.screen_w, self.screen_h, self.card_w, self.card_h)
        elif step in ["HEART", "❤"]:
            count = getattr(config, 'HEART_POINTS_COUNT', 70)
            return pattern.get_stroke_HEART(self.screen_w, self.screen_h, self.card_w, self.card_h, count=count)
        elif step == "W":
            return pattern.get_stroke_W(self.screen_w, self.screen_h, self.card_w, self.card_h)
        elif step == "Y":
            return pattern.get_stroke_Y(self.screen_w, self.screen_h, self.card_w, self.card_h)
        elif step == "M":
            return pattern.get_stroke_M(self.screen_w, self.screen_h, self.card_w, self.card_h)
        else:
            return pattern.get_stroke_HEART(self.screen_w, self.screen_h, self.card_w, self.card_h)

    def create_single_card(self, x: int, y: int, step_name: str):
        """创建一个独立的 macOS 风格精致小卡片"""
        if self.is_closing:
            return

        # 为每个框体生成独一无二的高雅配色与专属情话
        theme = get_unique_mac_theme(self.global_msg_index)
        message = config.LOVE_MESSAGES[self.global_msg_index % len(config.LOVE_MESSAGES)]
        self.global_msg_index += 1

        # 标签内容根据步骤进行专属提示
        step_titles = {
            "I": "Chapter I · 初见",
            "HEART": "Chapter II · 心动",
            "W": "Chapter III · 偏爱",
            "Y": "Chapter IV · 相守",
            "M": "Chapter V · 永恒"
        }
        tag = step_titles.get(step_name.upper(), "LoveOS · Memo")

        try:
            card = MacCardWindow(
                master=self.root,
                x=x,
                y=y,
                width=self.card_w,
                height=self.card_h,
                theme=theme,
                buttons_style=config.MAC_BUTTONS,
                message=message,
                tag_text=tag,
                animate=config.ENABLE_SMOOTH_ANIMATION,
                slide_offset=config.ANIMATION_SLIDE_OFFSET,
                anim_duration_ms=config.ANIMATION_DURATION_MS
            )
            self.current_step_cards.append(card)
            self.all_active_cards.append(card)
        except Exception:
            pass

    def play_step(self, step_idx: int):
        """播放当前步骤的书写过程"""
        if self.is_closing or step_idx >= len(self.steps):
            return

        step_name = self.steps[step_idx]
        points = self.get_step_points(step_name)
        total_pts = len(points)
        if total_pts == 0:
            self.next_step()
            return

        # 速度控制：心形生成速度放慢舒缓（50ms），字母流畅运笔（36ms）
        if step_name.upper() in ["HEART", "❤"]:
            interval = int(config.HEART_INTERVAL_MS * self.speed_multiplier)
        else:
            interval = int(config.LETTER_INTERVAL_MS * self.speed_multiplier)

        # 依次运笔书写生成小框体
        for idx, (px, py) in enumerate(points):
            aid = self.root.after(
                idx * interval,
                self.create_single_card,
                px, py, step_name
            )
            self.scheduled_after_ids.append(aid)

        # 书写完成后的定格等待时间 (最后一个字母 M 适当缩短，紧凑衔接终章烟花)
        stroke_finish_time = total_pts * interval
        if step_name.upper() == "M":
            hold_sec = getattr(config, 'STEP_M_HOLD_SECONDS', 0.7)
        else:
            hold_sec = getattr(config, 'STEP_HOLD_SECONDS', 1.1)
        hold_ms = int(hold_sec * 1000 * self.speed_multiplier)
        next_step_trigger_time = stroke_finish_time + hold_ms
        aid_next = self.root.after(next_step_trigger_time, self.transition_to_next_step)
        self.scheduled_after_ids.append(aid_next)

    def transition_to_next_step(self):
        """当前步骤结束：平滑淡出清空当前卡片，留白片刻后启动下一步骤或终章"""
        if self.is_closing:
            return

        fade_ms = config.STEP_FADE_OUT_MS
        # 1. 当前步骤卡片统一平滑淡出
        for card in self.current_step_cards:
            try:
                card.start_exit_animation(duration_ms=fade_ms)
            except Exception:
                pass

        # 2. 等待淡出彻底完成 + 留白呼吸感，然后清空并启动下一步
        delay_to_next = fade_ms + config.STEP_GAP_MS
        aid = self.root.after(delay_to_next, self._trigger_next_step_start)
        self.scheduled_after_ids.append(aid)

    def _trigger_next_step_start(self):
        """清空当前步卡片列表，启动下一步或终章全屏烟花"""
        if self.is_closing:
            return

        self.current_step_cards.clear()
        self.current_step_index += 1
        if self.current_step_index < len(self.steps):
            self.play_step(self.current_step_index)
        else:
            # 步骤 M 结束，进入终极压轴大结局
            if getattr(config, 'ENABLE_GRAND_FINALE', True):
                self.start_grand_finale()
            else:
                self.close_all(fast=False)

    def start_grand_finale(self):
        """【终极压轴】全屏烟花绽放 + Auth By William 赛博霓虹流光炫酷字体"""
        if self.is_closing:
            return

        duration = getattr(config, 'FINALE_DURATION_SECONDS', 12.0) * self.speed_multiplier

        try:
            self.finale_window = FinaleFireworksWindow(
                master=self.root,
                duration_seconds=duration,
                on_complete=lambda: self.close_all(fast=False)
            )
        except Exception:
            self.close_all(fast=False)

    def run(self):
        """启动整个浪漫手写叙事流程"""
        try:
            # 1. 禁用并隐藏鼠标（若配置开启）
            if self.disable_mouse:
                mouse_controller.lock()

            # 2. 从第一个步骤（"I"）开始深情书写
            self.current_step_index = 0
            self.finale_window = None
            self.play_step(0)

            # 3. 运行主事件循环
            self.root.mainloop()

        finally:
            self.close_all(fast=True)

    def close_all(self, fast: bool = False):
        """安全关闭所有窗体并恢复鼠标，具备强力看门狗保护"""
        if self.is_closing:
            return
        self.is_closing = True

        # 启动安全看门狗守护线程：若 1.5 秒后仍未退出，强行退出进程
        def _watchdog_exit():
            time.sleep(1.5)
            try:
                mouse_controller.unlock()
            except Exception:
                pass
            os._exit(0)

        threading.Thread(target=_watchdog_exit, daemon=True).start()

        # 销毁终章烟花窗口
        if hasattr(self, 'finale_window') and self.finale_window:
            try:
                self.finale_window.destroy()
            except Exception:
                pass

        try:
            # 1. 取消所有未执行的定时任务
            for aid in self.scheduled_after_ids:
                try:
                    self.root.after_cancel(aid)
                except Exception:
                    pass
            self.scheduled_after_ids.clear()

            # 2. 解除鼠标锁定，恢复光标
            mouse_controller.unlock()

            # 3. 销毁卡片（急速退出或平滑淡出）
            if fast or not config.ENABLE_SMOOTH_ANIMATION:
                self._destroy_all_cards_and_exit()
            else:
                fade_ms = getattr(config, 'STEP_FADE_OUT_MS', 250)
                for card in self.all_active_cards:
                    try:
                        card.start_exit_animation(duration_ms=fade_ms)
                    except Exception:
                        pass
                self.root.after(fade_ms + 40, self._destroy_all_cards_and_exit)
        except Exception:
            self._destroy_all_cards_and_exit()

    def _destroy_all_cards_and_exit(self):
        """彻底清理所有窗口资源并退出进程"""
        try:
            mouse_controller.unlock()
        except Exception:
            pass

        for card in self.all_active_cards:
            try:
                card.destroy()
            except Exception:
                pass
        self.all_active_cards.clear()
        self.current_step_cards.clear()

        try:
            self.root.quit()
            self.root.destroy()
        except Exception:
            pass

        os._exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="多窗口浪漫爱心与字母手写表白程序")
    parser.add_argument(
        "--no-lock",
        action="store_true",
        help="【调试模式】运行时不锁定鼠标"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="【快速调试模式】加快演播速度（用于快速校验全部步骤）"
    )
    args = parser.parse_args()

    multiplier = 0.25 if args.fast else 1.0

    app = MultiWindowLoveApp(
        no_mouse_lock=args.no_lock,
        speed_multiplier=multiplier
    )
    app.run()
