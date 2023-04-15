import pandas as pd
def cleanup_prepare_data(data):
    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)
    
    #getting only last ten years
    data = data.loc[data.index > "2010-01-10 01:01:00"]
    
    return data
