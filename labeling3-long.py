import os
import csv
import pandas as pd


def delete_unmatched_files(dir_path, csv_path):
    # Read the filenames from the CSV into a list
    df = pd.read_csv(csv_path, lineterminator='\n')
    csv_filenames = df.iloc[:, 0].tolist()  # Assuming filenames are in the first column

    # List all files in the directory
    dir_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    # Check each file against the list from the CSV and delete if not found in the CSV
    for file in dir_files:
        if file not in csv_filenames:
            if file == 'metadata.csv':
                continue
            os.remove(os.path.join(dir_path, file))
            print(f"Deleted: {file}")
            
            
def create_metadata_csv():
    dir = './logos3-long'
    csv_file = './logos3-long/metadata.csv'
    
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    len_count = {}
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['file_name', 'text'])
        
        long_name_csv = pd.read_csv('long_name_unique.csv', lineterminator='\n')
        
        for _, row in long_name_csv.iterrows():
            filename = row[0]  # Assuming the filename is in the first column
            filename_full = row[1]    # Assuming the prompt is in the second column        
            if filename in ['.DS_Store','metadata.csv','log.txt']:
                continue
            
            #exclude time and industry
            filename_clean = filename_full.replace('\n','').replace('\r', ' ')
            parts = filename_clean.split('_')
            len_count[len(parts)] = len_count.get(len(parts), 0 ) + 1
            print(filename_full)
            print(parts)
            print('-----------')
            print(filename_clean)
            print(f"part len = {len(parts)}")
            # [magic word] name, tags, industry, [magic word]
            if len(parts) > 2:
                part_1 = parts[0].replace('-', ' ').replace('\n','')                        #name
                part_2 = parts[2].replace('-', ' ').replace('\n', '').replace('.png', '')   #tags
                part_3 = parts[1].replace('_', ', ').replace('-', ' ').replace('\n', '')    #industry
                prompt = ('Simple elegant logo for ' + part_1 + ', ' + part_2 + ', ' + part_3).replace(',,', ',') + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges'
            elif len(parts) > 1:
                prompt = 'Simple elegant logo for ' + parts[0] + ' ' + parts[1].replace('.png', '') + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges'
            else:
                prompt = 'Simple elegant logo for ' + parts[0].replace('.png', '') + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges'

            writer.writerow([filename, prompt])
    
    print(f'len_count = {len_count}')
   
create_metadata_csv()
delete_unmatched_files('./logos3-long/', './logos3-long/metadata.csv')