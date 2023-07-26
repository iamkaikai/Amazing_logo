import os
import csv

words = ['lines', 'circles', 'triangles', 'dot', 'crosses', 'waves', 'square', '3D', 'Angled', 'Arrows', 'cube', 'Diamond', 'Hexagon', 'Loops', 'outline', 'ovals', 'rectangle', 'reflection', 'rings', 'round', 'semicircle', 'spiral', 'woven', 'stars']
shapes = [' Asymmetrical', ' Symmetrical', '']
pres = ['Simple elegant logo for Digital Art', 'Simple elegant logo for DA']
mid = 'D A '
suffix = ["successful vibe", "minimalist", "thought-provoking", "abstract", "recognizable", "black and white"]


dir = './'
csv_file = './prompt.csv'

with open(csv_file, 'w', newline='') as f:
    for word in words:
        for shape in shapes:
            for pre in pres:
                writer = csv.writer(f)
                prompt = [pre, mid + word + shape]
                for i in suffix:
                    prompt.append(i)
                writer.writerow(prompt)
