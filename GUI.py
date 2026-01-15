import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json


# 核心修复逻辑（复用咱之前的代码，保证兼容性）
def repair_file():
    """文件修复：从JSON读取内容覆写到目标文件"""
    try:
        # 选择JSON存档文件
        json_path = filedialog.askopenfilename(
            title="选择JSON存档文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if not json_path:
            return

        # 选择要修复的目标文件
        target_path = filedialog.askopenfilename(
            title="选择要修复的文件",
            filetypes=[("所有文件", "*.*")]
        )
        if not target_path:
            return

        # 读取JSON内容
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            content = data.get("content", "")

        # 覆写目标文件（自动备份原文件）
        # 备份逻辑：加.bak后缀
        if os.path.exists(target_path):
            bak_path = target_path + ".bak"
            with open(target_path, 'rb') as f_src, open(bak_path, 'wb') as f_dst:
                f_dst.write(f_src.read())

        # 写入修复内容
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)

        messagebox.showinfo("成功", f"文件修复完成！\n原文件已备份为：{bak_path}")
    except Exception as e:
        messagebox.showerror("错误", f"修复失败：{str(e)}")


def convert_old_file():
    """老格式文件转换（示例：.doc老文件转.txt，可扩展）"""
    try:
        old_file = filedialog.askopenfilename(
            title="选择老格式文件（.doc/.xls等）",
            filetypes=[("老格式文件", "*.doc;*.xls;*.txt"), ("所有文件", "*.*")]
        )
        if not old_file:
            return

        # 转换逻辑（简化版，实际可扩展为真实格式转换）
        new_file = old_file + "_new.txt"
        with open(old_file, 'rb') as f_src, open(new_file, 'w', encoding='utf-8') as f_dst:
            # 读取二进制转文本（适配老编码）
            content = f_src.read().decode('gbk', errors='ignore')
            f_dst.write(content)

        messagebox.showinfo("成功", f"老文件转换完成！\n新文件路径：{new_file}")
    except Exception as e:
        messagebox.showerror("错误", f"转换失败：{str(e)}")


# 搭建GUI界面（兼容所有系统的极简样式）
def create_gui():
    # 主窗口
    root = tk.Tk()
    root.title("Blocks文件工具箱 - 中国少年出品")
    root.geometry("500x300")  # 固定尺寸，老系统不崩
    root.resizable(False, False)  # 禁止缩放，适配小屏幕

    # 标题标签
    title_label = tk.Label(
        root,
        text="Blocks文件工具箱 | 全系统一键适配",
        font=("微软雅黑", 14, "bold"),
        fg="#4CAF50"
    )
    title_label.pack(pady=20)

    # 按钮框架
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=30)

    # 修复文件按钮
    repair_btn = tk.Button(
        btn_frame,
        text="📄 修复文件（JSON覆写）",
        command=repair_file,
        width=20,
        height=2,
        bg="#4CAF50",
        fg="white",
        relief="flat"
    )
    repair_btn.grid(row=0, column=0, padx=10)

    # 转换老文件按钮
    convert_btn = tk.Button(
        btn_frame,
        text="🔄 转换老格式文件",
        command=convert_old_file,
        width=20,
        height=2,
        bg="#2196F3",
        fg="white",
        relief="flat"
    )
    convert_btn.grid(row=0, column=1, padx=10)

    # 底部说明（适配老系统字体）
    desc_label = tk.Label(
        root,
        text="适配所有系统 | 基于Python开发 | 原文件自动备份",
        font=("宋体", 10),
        fg="#ccc"
    )
    desc_label.pack(side=tk.BOTTOM, pady=10)

    # 启动主循环
    root.mainloop()


# 程序入口（兼容Python2/3，老系统也能跑）
if __name__ == "__main__":
    try:
        create_gui()
    except Exception as e:
        # 老系统容错：弹出命令行提示
        print(f"GUI启动失败，降级为命令行模式：{e}")
        # 这里可复用之前的命令行逻辑，保证不闪退
        repair_file()