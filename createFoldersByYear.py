import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

# 照片所在的文件夹路径
source_folder = r"C:\Users\"  # 修改为你的路径

# 获取拍摄日期的方法
def get_taken_date(path):
    try:
        # 使用 piexif 获取 Exif 数据
        exif_dict = piexif.load(path)
        if '0th' in exif_dict and piexif.ImageIFD.DateTime in exif_dict['0th']:
            date_str = exif_dict['0th'][piexif.ImageIFD.DateTime].decode()
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        pass
    return None

# 创建文件夹并移动文件
def move_file_to_year_folder(filename, taken_date):
    # 使用年份作为文件夹名称
    folder_name = str(taken_date.year)
    
    # 创建目标文件夹路径
    target_folder = os.path.join(source_folder, folder_name)
    
    # 如果文件夹不存在，则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # 目标路径
    new_path = os.path.join(target_folder, filename)
    
    # 防止重名，自动加后缀
    i = 1
    while os.path.exists(new_path):
        new_name = taken_date.strftime(f"{taken_date.year}_%m-%d_%H-%M-%S") + f"_{i}" + os.path.splitext(filename)[1].lower()
        new_path = os.path.join(target_folder, new_name)
        i += 1
    
    # 移动文件
    shutil.move(os.path.join(source_folder, filename), new_path)
    print(f"文件 {filename} 移动到 {new_path}")

# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder):
    filepath = os.path.join(source_folder, filename)
    
    # 只处理图片文件（包括 CR2）
    if not os.path.isfile(filepath):
        continue
    
    # 获取拍摄日期
    taken_date = get_taken_date(filepath)
    if taken_date:
        # 将文件按年份分类并移动
        move_file_to_year_folder(filename, taken_date)
    else:
        print(f"未能提取拍摄日期: {filename}")
