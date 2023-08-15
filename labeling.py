import os
import csv

dir = './export_logo_512'
csv_file = './export_logo_512/metadata.csv'
len_count = {key: 0 for key in [1, 2, 3, 4]}

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_name', 'text'])
    
    for filename in os.listdir(dir):
        #exclude storage file and metadata.csv
        if filename in ['.DS_Store', 'metadata.csv', 'log.txt']:
            continue
        
        #exclude the country
        parts = filename.split('_')
        len_count[len(parts)] = len_count.get(len(parts),0) + 1
        
        if len(parts) > 4:
            print(filename)
            print(parts)
            print('-----------')
    
        # British-Tissues_United-Kingdom_Paper_B-Lines-T-United-kingdom.png,"name: British TissuesPaper, B Lines T United kingdom_logo"
        # output format = ... + name, keywords, industry + ... 
        if len(parts) > 4:
            part_1 = parts[0].replace('-', ' ')     #name
            part_3 = parts[len(parts)-2].replace('.png', '').replace('_', ', ').replace('-', ' ')   #industry    
            part_4 = parts[len(parts)-1].replace('.png', '').replace('_', ', ').replace('-', ' ')   #tags
            prompt = ('Simple elegant logo for ' + part_1 + ', ' + part_4 + ', ' + part_3 + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white').replace(',,', ',')
            print(f'>>>>> {prompt}')
            print('-----------')
        elif len(parts) > 3:
            part_1 = parts[0].replace('-', ' ').replace(',', '')    #name
            part_2 = parts[2].replace('-', ' ')                     #industry
            part_3 = parts[3].replace('.png', '').replace('_', ', ').replace('-', ' ').replace(',', '')    #tags
            prompt = ('Simple elegant logo for ' + part_1 + ', ' + part_3 + ', ' + part_2 + ', successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white').replace(',,', ',')
        
        else:
            prompt = 'Simple elegant logo for ' + parts[0].replace('-', ' ').replace('.png', ' successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white')

        writer.writerow([filename, prompt])
    
    print(len_count)

# prompt
# a clean black logo of Digital Art on a white background, graphic design, logomarks, logo collection, portfolio, trademark, monogram, logotype, brand identity, visual identity
# Simple elegant logo for a [company], [eagle], successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges