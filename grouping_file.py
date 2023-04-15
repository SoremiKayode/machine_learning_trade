import os
import shutil
os.path.join
def group_file(folder, file_alias):
    dir = os.listdir(folder)
    all_file = [os.path.join(folder, x) for x in dir if file_alias in x]
    new_folder_dir = f"{file_alias}1MINUTE"
    os.mkdir(new_folder_dir)
    for files in all_file :
        shutil.move(files, new_folder_dir)
        
    

all_alias = ["USDCHF", "NZDUSD", "USDJPY"]

for alias in all_alias :
    group_file("C:/Users/DELL/Downloads", alias)