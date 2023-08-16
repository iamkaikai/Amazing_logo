import os
import csv

dir = './export_logo2_512'
csv_file = './export_logo2_512/metadata.csv'
len_count = {}

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_name', 'text'])
    
    for filename in os.listdir(dir):
        #exclude storage file and metadata.csv
        if filename == '.DS_Store' or filename == 'metadata.csv':
            continue
        
        #exclude time and industry
        parts = filename.split('_')
        len_count[len(parts)] = len_count.get(len(parts),0) + 1
        print(filename)
        print(parts)
        print('-----------')
        
        # British-Tissues_United-Kingdom_Paper_B-Lines-T-United-kingdom.png,"name: British TissuesPaper, B Lines T United kingdom_logo"

        if len(parts) > 2:
            part_1 = parts[0].replace('-', ' ')     #name
            part_2 = parts[1].split('-')
            part_2 = [word for idx, word in enumerate(part_2) if idx != 0 and not word[0].isdigit()]
            part_2 = ' '.join(part_2)
            # part_2 = parts[1].replace('-', ' ')     #keep only industry
            part_3 = parts[2].replace('.png', '').replace('_', ', ').replace('-', ' ').replace(',','')    #tags
            prompt = ('Simple elegant logo for ' + part_1 + ', ' + part_3 + ', ' + part_2 + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white').replace(',,', ',')
        
        elif len(parts) > 1:
            part_1 = parts[0].replace('-', ' ').replace(',','')
            part_2 = parts[1].replace('.png', '_successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white').replace('_', ',').replace('-', ' ').replace(',','')
            prompt = ('Simple elegant logo for ' + part_1 + ',' + part_2).replace(',,', ',')
            print(f'>>>>> {prompt}')
            print('-----------')
        else:
            prompt = 'Simple elegant logo for ' + parts[0].replace('-', ' ').replace('.png', ' successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white')

        writer.writerow([filename, prompt])

print(len_count)
# prompt
# a clean black logo of Digital Art on a white background, graphic design, logomarks, logo collection, portfolio, trademark, monogram, logotype, brand identity, visual identity
# Simple elegant logo for a [company], [eagle], successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges