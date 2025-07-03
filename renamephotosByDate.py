from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime

# 设置原始文件夹路径
source_folder = r"C:\Users\wewer\OneDrive\Pictures\huifu\101CANON"

# 获取拍摄日期的方法
def get_taken_date(path):
    try:
        image = Image.open(path)
        exif = image._getexif()
        if exif:
            for tag, value in exif.items():
                tag_name = TAGS.get(tag)
                if tag_name == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        pass
    return None

# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder):
    filepath = os.path.join(source_folder, filename)
    
    # 只处理图片文件
    if not os.path.isfile(filepath):
        continue
    
    # 获取拍摄日期
    taken_date = get_taken_date(filepath)
    if taken_date:
        # 按拍摄日期格式化新文件名
        new_name = taken_date.strftime("%Y-%m-%d_%H-%M-%S") + os.path.splitext(filename)[1].lower()
        new_path = os.path.join(source_folder, new_name)
        
        # 防止重名，自动加后缀
        i = 1
        while os.path.exists(new_path):
            new_name = taken_date.strftime("%Y-%m-%d_%H-%M-%S") + f"_{i}" + os.path.splitext(filename)[1].lower()
            new_path = os.path.join(source_folder, new_name)
            i += 1
        
        # 重命名文件
        os.rename(filepath, new_path)
        print(f"重命名: {filename} → {new_name}")
    else:
        print(f"未能提取拍摄日期: {filename}")
