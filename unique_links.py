import difflib

def print_differences(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        # Read the lines of each file
        f1_lines = set(f1.readlines())
        f2_lines = set(f2.readlines())

         # Print lines only in file 1
        for line in f1_lines - f2_lines:
            print(f'- {line}', end='')

        # Print lines only in file 2
        for line in f2_lines - f1_lines:
            print(f'+ {line}', end='')

print_differences('links.txt', 'downloaded.txt')
