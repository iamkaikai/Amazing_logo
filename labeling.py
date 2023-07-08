import os
import csv

dir = './amazing_logos/data'
csv_file = './amazing_logos/data/metadata.csv'
# csv_file = './amazing_logos/dataset/a.csv'

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_name', 'text'])
    # Alfa_Poland_Chemicals_Hexagon-Poland-Triangles.png,name: AlfaPoland
    
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
            part_2 = parts[2].replace('.png', '_logo').replace('_', ', ').replace('-', ' ')
            prompt = "name: " + (part_1 + ', ' + part_2).replace(',,', ',')
        elif len(parts) > 1:
            part_1 = parts[0].replace('-', ' ')
            part_2 = parts[1].replace('.png', '_logo').replace('-', ' ')
            prompt = "name: " + (part_1 + ', ' +part_2).replace(',,', ',')
        else:
            prompt = "name: " + parts[0].replace('-', ' ').replace('.png', ', logo')

        writer.writerow([filename, prompt])
