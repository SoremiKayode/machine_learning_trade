from zipfile import ZipFile
import os
import sort_merge
import shutil

# print()

def unzip_file(filepath, filedirectory):
    if not os.path.exists(filedirectory):
        os.mkdir(filedirectory)
    if os.path.exists(filepath):
        for files in os.listdir(filepath):
            if files.endswith(".zip"):
                with ZipFile(f"{filepath}/{files}", "r") as zip_file:
                    zip_file.extractall(path=filedirectory)
                    
                    print(f"{files} has been successfully extracted")
        shutil.rmtree(filepath)
    # sort_merge.sort_merge_file(filedirectory, filepath)
       
all_files = ["USDCHF1MINUTE", "NZDUSD1MINUTE", "USDJPY1MINUTE",
             "GBPUSD1MINUTE", "USDCAD1MINUTE",
             "XAUUSD1MINUTE", "AUDUSD1MINUTE"]

for filer in all_files: 
    unzip_file(filer, f"{filer}_UNZIPPED")