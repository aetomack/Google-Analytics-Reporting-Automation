import pandas as pd
import os 

folder_path = r'datapathway'
all_files = os.listdir(folder_path)

def clean_columns(dataframe):
    for col in dataframe.columns:
        if col.startswith("ga:"):
                newcol = col[3:]
                dataframe.rename(columns={col:newcol}, inplace=True)
    return dataframe

def clean_entry(entry):
    if entry.startswith("b'") and entry.endswith("'"):
        return entry[2:-1]
    else:
        return entry
    
def clean_frame(dataframe):
    for col in dataframe.columns:
        for i in range(len(dataframe)):
            item = dataframe.loc[i, col]
            dataframe.loc[i, col] = clean_entry(item)
           
           
            
for dir in all_files:
    folder_path = r'datapath\%s' % dir
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    clean_path = r'datapath\%s' %str(dir)
    os.makedirs(clean_path)
    
    for csv in csv_files:
        file_path = os.path.join(folder_path,csv)
        name = csv.replace(".csv","")[2:]
        
        try:
            df = pd.read_csv(file_path)
            clean_frame(clean_columns(df))
                    

        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, sep = '/t', encoding='utf-16')
                clean_frame(clean_columns(df))

            except Exception as e:
                print(f"Could not read CSV 1: "+name)
                
        except Exception as e: 
            print(f"Could not read CSV 2: "+name)

        df.to_csv(os.path.join(clean_path, name+'.csv'), index=False)