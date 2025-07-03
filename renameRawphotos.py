import piexif
from PIL import Image
import os
from datetime import datetime

source_folder = r"C:\Users\"  

# get shooting dates
def get_taken_date(path):
    try:
        # use piexif for getting Exif data
        exif_dict = piexif.load(path)
        if '0th' in exif_dict and piexif.ImageIFD.DateTime in exif_dict['0th']:
            date_str = exif_dict['0th'][piexif.ImageIFD.DateTime].decode()
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        pass
    return None

# go through all files
for filename in os.listdir(source_folder):
    filepath = os.path.join(source_folder, filename)
    
    # only process photos including CR
    if not os.path.isfile(filepath):
        continue
    
    # get taken dates
    taken_date = get_taken_date(filepath)
    if taken_date:
        # rename by dates
        new_name = taken_date.strftime("%Y-%m-%d_%H-%M-%S") + os.path.splitext(filename)[1].lower()
        new_path = os.path.join(source_folder, new_name)
        
        # Prevent duplicate names, add suffixes
        i = 1
        while os.path.exists(new_path):
            new_name = taken_date.strftime("%Y-%m-%d_%H-%M-%S") + f"_{i}" + os.path.splitext(filename)[1].lower()
            new_path = os.path.join(source_folder, new_name)
            i += 1
        
        # rename
        os.rename(filepath, new_path)
        print(f"rename: {filename} → {new_name}")
    else:
        print(f"can not get dates: {filename}")
