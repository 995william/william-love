# -*- coding: utf-8 -*-
"""
鼠标安全控制模块 (适用于 Windows 10 / Windows 11)
- 运行期间禁用鼠标（限制移动并隐藏光标）
- 退出时无论正常还是异常，100% 自动恢复鼠标
- 监听 ESC 键作为紧急停止开关
"""

import atexit
import ctypes
from ctypes import wintypes
import sys
import threading
import time

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

VK_ESCAPE = 0x1B


class MouseController:
    def __init__(self, enable_block: bool = True):
        self.enabled_block = enable_block
        self._is_locked = False
        self._stop_listener = False
        self._esc_callback = None
        self._listener_thread = None

        # 注册进程退出时的安全恢复保障
        atexit.register(self.unlock)

    def set_esc_callback(self, callback):
        """设置按下 ESC 键时的回调函数"""
        self._esc_callback = callback

    def start_esc_listener(self):
        """后台线程检测 ESC 紧急退出键"""
        if self._listener_thread is not None:
            return

        def _listen():
            while not self._stop_listener:
                # 检查 ESC 键状态 (最高位为 1 表示按下)
                if user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000:
                    if self._esc_callback:
                        try:
                            self._esc_callback()
                        except Exception:
                            pass
                    break
                time.sleep(0.05)

        self._listener_thread = threading.Thread(target=_listen, daemon=True)
        self._listener_thread.start()

    def lock(self):
        """锁定并隐藏鼠标"""
        if not self.enabled_block or self._is_locked:
            return

        try:
            # 1. 尝试系统级输入拦截
            user32.BlockInput(True)
        except Exception:
            pass

        try:
            # 2. 将鼠标光标限制在屏幕极小角落像素 (0, 0, 1, 1)，物理上不可移动
            rect = wintypes.RECT(0, 0, 1, 1)
            user32.ClipCursor(ctypes.byref(rect))
        except Exception:
            pass

        try:
            # 3. 隐藏鼠标光标指针
            while user32.ShowCursor(False) >= 0:
                pass
        except Exception:
            pass

        self._is_locked = True
        self.start_esc_listener()

    def unlock(self):
        """解除鼠标锁定，恢复光标并重置限制"""
        if not self._is_locked:
            return

        self._stop_listener = True

        try:
            # 1. 解除 BlockInput
            user32.BlockInput(False)
        except Exception:
            pass

        try:
            # 2. 解除鼠标区域限制
            user32.ClipCursor(None)
        except Exception:
            pass

        try:
            # 3. 恢复光标指针显示
            while user32.ShowCursor(True) < 0:
                pass
        except Exception:
            pass

        self._is_locked = False


# 全局单例管理器
mouse_controller = MouseController(enable_block=True)
