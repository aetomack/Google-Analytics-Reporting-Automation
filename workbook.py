import os
import pandas as pd
import time

file_path = r'path containing directories of folders related to each site export'

def get_dirs(path):
    return os.listdir(path)

def get_csvs(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.csv')]

def combine_csvs(csv_files, output_dir):
    output_file = os.path.join(output_dir, 'combined.xlsx')
    writer = pd.ExcelWriter(output_file)
    for idx, csv_file in enumerate(csv_files, start=1):
        df = pd.read_csv(csv_file)
        sheet_name = os.path.splitext(os.path.basename(csv_file))[0]
        df.to_excel(writer, sheet_name=sheet_name)
        if idx % 10 == 0:  # Print elapsed time every 10 files
            print(f"Processed {idx} files...")
            print_elapsed_time()
    writer.close()

def print_elapsed_time():
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

def main():
    global start_time
    start_time = time.time()  # Start timer
    for dir_name in get_dirs(file_path):
        dir_path = os.path.join(file_path, dir_name)
        csv_files = get_csvs(dir_path)
        combine_csvs(csv_files, dir_path)
    print("Script execution completed.")
    print_elapsed_time()  # Print final elapsed time

if __name__ == "__main__":
    main()
