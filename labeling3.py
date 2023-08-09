import os
import csv

def create_metadata_csv():
    dir = './logos3'
    csv_file = './logos3/metadata.csv'
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['file_name', 'text'])
        
        for filename in os.listdir(dir):
            #exclude storage file and metadata.csv
            if filename == '.DS_Store' or filename == 'metadata.csv':
                continue
            
            #exclude time and industry
            filename_clean = filename.replace('\n','').replace('\r', ' ')
            parts = filename_clean.split('_')
            print(filename)
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

    # prompt
    # a clean black logo of Digital Art on a white background, graphic design, logomarks, logo collection, portfolio, trademark, monogram, logotype, brand identity, visual identity
    # Simple elegant logo for a [company], [eagle], successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges