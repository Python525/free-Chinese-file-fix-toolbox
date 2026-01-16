import json
import os
from datetime import datetime


def archive_py_to_json(py_file_path, json_file_path):
    """
    将Python文件的内容和元信息存档到JSON文件
    :param py_file_path: 待存档的.py文件路径
    :param json_file_path: 输出的.json文件路径
    """
    # 校验.py文件是否存在，避免报错
    if not os.path.exists(py_file_path):
        print(f"❌ ERROR ：文件 {py_file_path} was not bi found!")
        return False

    try:
        # 读取.py文件的文本内容（核心修复点）
        with open(py_file_path, 'r', encoding='utf-8') as file_py:
            py_content = file_py.read()  # 读取文件内容为字符串

        # 收集文件元信息（方便后续修复器校验）
        file_stat = os.stat(py_file_path)
        archive_data = {
            "file_name": os.path.basename(py_file_path),  # 文件名（如绘图器.py）
            "file_path": os.path.abspath(py_file_path),  # 绝对路径
            "archive_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 存档时间
            "file_size": file_stat.st_size,  # 文件大小（字节）
            "content": py_content  # 核心：文件的实际代码内容
        }

        # 将信息写入JSON文件
        with open(json_file_path, 'w', encoding='utf-8') as file_json:
            json.dump(archive_data, file_json, ensure_ascii=False, indent=4)

        print(f"✅ OK：{py_file_path} → {json_file_path}")
        return True

    except Exception as e:
        print(f"❌ Failed to save {py_file_path}：{str(e)}")
        return False


# 批量存档你的所有Python文件（精简代码，避免重复写with open）
file_list = [
    ("DOS基本计算.py", "001.json"),
    ("记事本.py", "002.json"),
    ("回收站.py", "003.json"),
    ("计时器.py", "004.json"),
    ("信息树.py", "005.json"),
    ("绘图器.py", "006.json"),
    ("文件存档器.py", "007.json"),
    ("文件修复器.py", "008.json")
]

# 执行批量存档
for py_file, json_file in file_list:
    archive_py_to_json(py_file, json_file)
