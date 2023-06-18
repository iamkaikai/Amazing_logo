import re
file = "logobook.html"

with open(file, 'r') as f:
    content = f.read()

# pattern = r'http://www\.logobook\.com/letter/([a-z]/|number-logos/all/)'
# pattern = r'(http://www\.logobook\.com/letter/[a-z]/|http://www\.logobook\.com/number-logos/all/|http://www\.logobook\.com/shape/[0-9a-z]*/)'
pattern = r'(http://www\.logobook\.com/(letter/[a-z]/|number-logos/all/|shape/[0-9a-z]*/|object/[0-9a-z\-]*|nature/[0-9a-z\-]*|business/[0-9a-z\-]*))'

matches = set(re.findall(pattern, content))


with open("links.txt", "w") as f:
    for link in matches:
       f.write(str(link[0]) + '\n')
        
print("saving file...")
