import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime


class FileArchiveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python文件备份工具")
        self.root.geometry("550x280")
        self.root.resizable(False, False)

        # 初始化变量
        self.selected_file_path = tk.StringVar()  # 选中的文件路径
        self.archive_index = tk.StringVar(value="1")  # 备份序号，默认1

        # 创建UI组件
        self._create_widgets()

    def _create_widgets(self):
        # 1. 文件选择区域
        frame_file = ttk.LabelFrame(self.root, text="文件选择", padding=(10, 5))
        frame_file.place(x=20, y=20, width=510, height=80)

        ttk.Label(frame_file, text="选中文件：").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame_file, textvariable=self.selected_file_path, state="readonly", width=50).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Button(frame_file, text="选择文件", command=self.select_file).grid(
            row=0, column=2, padx=5, pady=5
        )

        # 2. 备份序号设置区域
        frame_index = ttk.LabelFrame(self.root, text="备份序号设置", padding=(10, 5))
        frame_index.place(x=20, y=110, width=510, height=80)

        ttk.Label(frame_index, text="备份序号：").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame_index, textvariable=self.archive_index, width=10).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Label(frame_index, text="（示例：输入39则生成039.json）").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )

        # 3. 执行备份按钮
        ttk.Button(
            self.root, text="执行备份", command=self.archive_file, style="Accent.TButton"
        ).place(x=200, y=210, width=150, height=40)

    def select_file(self):
        """打开文件选择框，选择要备份的.py文件"""
        file_path = filedialog.askopenfilename(
            title="选择要备份的Python文件",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        if file_path:
            self.selected_file_path.set(file_path)

    def archive_file(self):
        """执行文件备份逻辑"""
        # 1. 校验输入
        py_file_path = self.selected_file_path.get().strip()
        if not py_file_path:
            messagebox.showerror("错误", "请先选择要备份的文件！")
            return

        try:
            index = int(self.archive_index.get().strip())
            if index < 1 or index > 999:
                messagebox.showerror("错误", "备份序号请输入1-999之间的整数！")
                return
        except ValueError:
            messagebox.showerror("错误", "备份序号必须是整数！")
            return

        # 2. 生成JSON文件名（补零为3位，如3→003.json）
        json_file_name = f"{index:03d}.json"
        json_file_path = os.path.join(os.path.dirname(py_file_path), json_file_name)

        # 3. 读取并备份文件
        try:
            # 读取Python文件内容
            with open(py_file_path, 'r', encoding='utf-8') as f:
                py_content = f.read()

            # 收集文件元信息
            file_stat = os.stat(py_file_path)
            archive_data = {
                "file_name": os.path.basename(py_file_path),
                "file_path": os.path.abspath(py_file_path),
                "archive_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": file_stat.st_size,
                "content": py_content,
                "archive_index": index  # 记录备份序号
            }

            # 写入JSON文件
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(archive_data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("成功", f"备份完成！\n原文件：{py_file_path}\n备份文件：{json_file_path}")
            # 清空选择（可选）
            self.selected_file_path.set("")
            self.archive_index.set(str(index + 1))  # 序号自动+1，方便下次使用

        except FileNotFoundError:
            messagebox.showerror("错误", f"文件 {py_file_path} 不存在！")
        except PermissionError:
            messagebox.showerror("错误", f"无权限访问文件 {py_file_path} 或写入备份文件！")
        except Exception as e:
            messagebox.showerror("错误", f"备份失败：{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    # 美化按钮样式（可选）
    style = ttk.Style(root)
    style.configure("Accent.TButton", font=("微软雅黑", 10, "bold"))
    app = FileArchiveGUI(root)
    root.mainloop()