# -*- coding: utf-8 -*-
"""
单文件独立 EXE 自动编译与打包脚本 (纯 Python 驱动，彻底解决 CMD 批处理中文乱码)
兼容 Windows 10 与 Windows 11
"""

import os
import shutil
import subprocess
import sys


def main():
    print("=" * 65)
    print("  正在执行多窗口告白程序单文件打包 (PyInstaller)")
    print("  目标系统：Windows 10 / Windows 11 (64-bit)")
    print("=" * 65)

    tools_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(tools_dir)
    os.chdir(root_dir)

    icon_path = os.path.join(root_dir, "assets", "heart.ico")
    main_py_path = os.path.join(root_dir, "main.py")

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "-F",
        "-w",
        f"--icon={icon_path}" if os.path.exists(icon_path) else "",
        "--clean",
        "--name=爱心告白多窗口",
        main_py_path
    ]
    cmd = [c for c in cmd if c]

    print("\n[1/3] 正在使用 PyInstaller 进行静态打包封装，请稍候...")
    ret = subprocess.run(cmd)
    if ret.returncode != 0:
        print("\n[错误] PyInstaller 编译失败！退出码:", ret.returncode)
        return ret.returncode

    # 复制副本 LoveApp.exe (双保险英文名镜像)
    dist_dir = os.path.join(root_dir, "dist")
    target_cn = os.path.join(dist_dir, "爱心告白多窗口.exe")
    target_en = os.path.join(dist_dir, "LoveApp.exe")
    if os.path.exists(target_cn):
        try:
            shutil.copyfile(target_cn, target_en)
        except Exception:
            pass

    # 清理临时构建缓存与 .spec 临时文件
    print("\n[2/3] 正在清理临时构建缓存与中间文件...")
    build_dir = os.path.join(root_dir, "build")
    if os.path.exists(build_dir):
        try:
            shutil.rmtree(build_dir, ignore_errors=True)
        except Exception:
            pass

    for fname in os.listdir(root_dir):
        if fname.endswith(".spec"):
            try:
                os.remove(os.path.join(root_dir, fname))
            except Exception:
                pass

    print("\n[3/3] 打包大功告成！")
    print("=" * 65)
    print("  独立单文件可执行程序已输出至 dist 目录：")
    print(f"  [中文名称] {target_cn}")
    print(f"  [英文镜像] {target_en}")
    print("=" * 65)
    return 0


if __name__ == "__main__":
    sys.exit(main())
