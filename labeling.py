import os
import csv

dir = './huggingface/amazing_logos/data'
csv_file = './huggingface/amazing_logos/data/metadata.csv'

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_name', 'text'])
    
    for filename in os.listdir(dir):
        #exclude the country
        parts = filename.split('_', 2)
        print(filename)
        print(parts)
        print('-----------')
        
        # British-Tissues_United-Kingdom_Paper_B-Lines-T-United-kingdom.png,"name: British TissuesPaper, B Lines T United kingdom_logo"
        # output format = name:xxxx, sector(optional), keywords(seperate with spaces), logo 
        if len(parts) > 2:
            part_1 = parts[0].replace('-', ' ')
            part_2 = parts[2].replace('.png', '_successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges').replace('_', ', ').replace('-', ' ')
            prompt = ('Simple elegant logo for a ' + part_1 + part_2).replace(',,', ',')
        elif len(parts) > 1:
            part_1 = parts[0].replace('-', ' ')
            part_2 = parts[1].replace('.png', '_successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges').replace('_', ', ').replace('-', ' ')
            prompt = ('Simple elegant logo for a ' + part_1 + part_2).replace(',,', ',')
        else:
            prompt = 'Simple elegant logo for a ' + parts[0].replace('-', ' ').replace('.png', ' successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges')

        writer.writerow([filename, prompt])

# prompt
# a clean black logo of Digital Art on a white background, graphic design, logomarks, logo collection, portfolio, trademark, monogram, logotype, brand identity, visual identity
# Simple elegant logo for a [company], [eagle], successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges