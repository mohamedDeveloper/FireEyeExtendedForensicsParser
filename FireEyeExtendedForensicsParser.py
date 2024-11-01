import zipfile
import os
import sys 
import pandas as pd
import json
import re
import shutil


df = pd.DataFrame()

file_keys = [
    ['"PowerShellHistoryItem":', "PowerShellHistory"], 
    ['"TaskFileName":', "ScheduledTasks"], 
    ['"PrefetchItemExtended":', "Prefetch"],  
    ['"ProcessItem":', "Processes"], 
    ['"YaraMatchData":', "yaraResults"], 
    ['"w32scripting-amcache"', "Amcache"],
    ['"w32scripting-recyclebin",' ,"Recycle Bin"]
]



def delete_zip_files_and_folders(directory):

    if not os.path.isdir(directory):
        print(f'The path provided is not a directory: {directory}')
        return
    

    for root, dirs, files in os.walk(directory):

        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f'Deleted file: {file_path}')
                except Exception as e:
                    print(f'Could not delete file {file_path}: {e}')
        

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                shutil.rmtree(dir_path)
                print(f'Deleted directory: {dir_path}')
            except Exception as e:
                print(f'Could not delete directory {dir_path}: {e}')



def find_files_with_keyword(directory, keyword):
    fileNames = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if keyword in content:
                        fileNames.append(file_path)
                        print(f'Found in: {file_path}')
            except Exception as e:
                print(f'Could not read {file_path}: {e}')
    
    return fileNames

def unzip_file(zip_file, output_dir):
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(output_dir)
        print(f"Extracted: {zip_file} to {output_dir}")
        

        for file_info in z.infolist():
            if file_info.filename.endswith('.zip'):
                nested_zip_path = os.path.join(output_dir, file_info.filename)

                with z.open(file_info) as nested_zip_file:
                    with zipfile.ZipFile(nested_zip_file) as nested_zip:

                        nested_output_dir = os.path.join(output_dir, os.path.splitext(file_info.filename)[0])
                        os.makedirs(nested_output_dir, exist_ok=True)

                        nested_zip.extractall(nested_output_dir)
                        print(f"Extracted nested ZIP: {file_info.filename} to {nested_output_dir}")

                        unzip_file(nested_zip_path, nested_output_dir)

def delete_directory_if_exists(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)
        print(f'Deleted directory: {directory}')
    else:
        print(f'Directory does not exist: {directory}')


def extract_prefix(path):

    parent_directory = os.path.dirname(path)
    

    last_dir = os.path.basename(parent_directory)

    result = last_dir.split('_')[0]
    
    return result

def json_to_csv(json_file_path, csv_file_path):
    global df 
    print("قيمة المتغير هي:", json_file_path)
    print("قيمة المتئئئئئغير هي:", csv_file_path)


    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path, low_memory=False)
    else:
        df = pd.DataFrame() 
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            content = json_file.read()
    except UnicodeDecodeError:
        with open(json_file_path, 'r', encoding='latin-1') as json_file:
            content = json_file.read()


    match = re.search(r'\[.*(?=.$)', content, re.DOTALL)
    if match:
        json_data = json.loads(match.group(0))
    else:
        print("No valid JSON array found in the file.")
        return

    new_df = pd.json_normalize(json_data)
    hostName = extract_prefix(json_file_path)
    new_df.insert(0, 'Host Name', [hostName] * len(new_df))

    df = pd.concat([df, new_df], ignore_index=True)

    df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_to_csv.py <input_json_file> <output_csv_file>")
        sys.exit(1)

    zip_file = sys.argv[1]    
    output_dir2 = zip_file[:-4] if zip_file.endswith(".zip") else zip_file
    print(output_dir2)

    script_path = os.path.abspath(sys.argv[0])
    output_dir3 = os.path.dirname(script_path)
    output_dir = os.path.join(output_dir3, output_dir2)  
    delete_directory_if_exists(output_dir)
    if os.path.isfile(zip_file) and zip_file.endswith('.zip'):
        os.makedirs(output_dir, exist_ok=True)  
        unzip_file(zip_file, output_dir)
        
        for i in range(len(file_keys)): 
            fileNames = find_files_with_keyword(output_dir, file_keys[i][0])
            df = pd.DataFrame()                  
            
            for fileName in fileNames:
                dest2 = file_keys[i][1] + ".csv"
                dest = os.path.join(output_dir, dest2) 
                json_to_csv(fileName, dest)   
      
    else:
        print("Invalid ZIP file path.")
    delete_zip_files_and_folders(output_dir)
