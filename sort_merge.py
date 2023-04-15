import os
import shutil
import pandas as pd
def sort_merge_file(directory, output_filename):
    # Getting all the csv files in the directory
    all_csv_file = [file for file in os.listdir(directory) if file.endswith(".csv")]
    # sorting the list in ascending order
    all_csv_file.sort()
    # create a variable that will hold the joined dataframe
    merge_data = None
    
    #looping through all the csv files and concatenating them to the previous, or previously joined
    for dat in range(len(all_csv_file)):
        data = pd.read_csv(f"{directory}/{all_csv_file[dat]}", names=["Date", "Open", "High", "Low", "Close", "Tick"], delimiter=";")
        # data["Date"] = data[["Date", "Time"]].apply(".".join, axis=1)
        data["Date"] = pd.to_datetime(data["Date"])
        # data["Date"] = pd.to_datetime(data['Date'] + data['Time'], format='%Y-%m-%d.%H:%M:%S')
        # data.drop("Time", axis=1, inplace=True)
        data.set_index("Date", inplace=True)
        
        if merge_data is not None :
            frames =[merge_data, data]
            result = pd.concat(frames)
            merge_data = result
        else :
            merge_data = data
        print(F"The lenght of {dat} dataset is {len(data)}")
        print(F"{dat} dataset concatenated current lenght of dataset is {len(merge_data)}")
        
    merge_data.to_csv(f"{output_filename}.csv")

all_files = ["NZDUSD1MINUTE", "USDJPY1MINUTE",
             "GBPUSD1MINUTE", "USDCAD1MINUTE",
             "XAUUSD1MINUTE", "AUDUSD1MINUTE"]

for files in all_files :  
    sort_merge_file(f"{files}_UNZIPPED", files)
    print("================================================")
    print(f"{files} downe joining")
    print("================================================")

