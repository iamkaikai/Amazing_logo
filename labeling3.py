import os
import csv

dir = './logos3'
csv_file = './logos3/metadata.csv'

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_name', 'text'])
    
    for filename in os.listdir(dir):
        #exclude storage file and metadata.csv
        if filename == '.DS_Store' or filename == 'metadata.csv':
            continue
        
        #exclude time and industry
        filename = filename.replace('\n','').replace('\r', ' ')
        parts = filename.split('_')
        print(filename)
        print(parts)
        print('-----------')
        
        # [magic word] name, tags, industry, [magic word]
        if len(parts) > 1:
            part_1 = parts[0].replace('-', ' ').replace('\n','')                        #name
            part_2 = parts[2].replace('-', ' ').replace('\n', '')                       #tags
            part_3 = parts[1].replace('_', ', ').replace('-', ' ').replace('\n', '')    #industry
            prompt = ('Simple elegant logo for ' + part_1 + ', ' + part_2 + ', ' + part_3).replace(',,', ',') + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges'
        else:
            prompt = 'Simple elegant logo for ' + parts[0] + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges'

        writer.writerow([filename, prompt])

# prompt
# a clean black logo of Digital Art on a white background, graphic design, logomarks, logo collection, portfolio, trademark, monogram, logotype, brand identity, visual identity
# Simple elegant logo for a [company], [eagle], successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges