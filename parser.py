import re

file = "logobook.html"

with open(file, 'r') as f:
    content = f.read()

# pattern = r'http://www\.logobook\.com/letter/([a-z]/|number-logos/all/)'
pattern = r'(http://www\.logobook\.com/letter/[a-z]/|http://www\.logobook\.com/letter/number-logos/all/)'



matches = re.findall(pattern, content)

with open("links.txt", "w") as f:
    for link in matches:
        f.write(link + '\n')
        
print("saving file...")
