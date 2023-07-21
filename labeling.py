import os
import csv

dir = './export_logo_512'
csv_file = './export_logo_512/metadata.csv'

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_name', 'text'])
    
    for filename in os.listdir(dir):
        #exclude storage file and metadata.csv
        if filename == '.DS_Store' or filename == 'metadata.csv':
            continue
        
        #exclude the country
        parts = filename.split('_', 2)
        print(filename)
        print(parts)
        print('-----------')
        
        # British-Tissues_United-Kingdom_Paper_B-Lines-T-United-kingdom.png,"name: British TissuesPaper, B Lines T United kingdom_logo"
        # output format = name:xxxx, sector(optional), keywords(seperate with spaces), logo 
        if len(parts) > 2:
            part_1 = parts[0].replace('-', ' ')
            part_2 = parts[2].replace('.png', '_successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white').replace('_', ', ').replace('-', ' ')
            prompt = ('Simple elegant logo for ' + part_1 + part_2).replace(',,', ',')
        elif len(parts) > 1:
            part_1 = parts[0].replace('-', ' ')
            part_2 = parts[1].replace('.png', '_successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white').replace('_', ', ').replace('-', ' ')
            prompt = ('Simple elegant logo for ' + part_1 + part_2).replace(',,', ',')
        else:
            prompt = 'Simple elegant logo for ' + parts[0].replace('-', ' ').replace('.png', ' successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges, black and white')

        writer.writerow([filename, prompt])

# prompt
# a clean black logo of Digital Art on a white background, graphic design, logomarks, logo collection, portfolio, trademark, monogram, logotype, brand identity, visual identity
# Simple elegant logo for a [company], [eagle], successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges