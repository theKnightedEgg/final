import sys

choices = 0
title = ""
labels = []
payoffs = []


for line in open(sys.argv[1]):
    line = line.strip()
    if line != "" and not line.startswith("#"):
        if choices == 0:
            choices = (int) (line)
        elif title == "":
            title = line
        else:
            line_contents = line.split()
            labels.append(line_contents[0])
            line_contents = line_contents[1:]
            row = []
            for i in range(len(line_contents) // 2):
                row.append((line_contents[i*2], line_contents[i*2 + 1]))
            payoffs.append(row)
            print(line_contents)

print(f"Choices: {choices}")
print(f"Title: {title}")
print(f"Labels: {labels}")
print(f"Payoffs: {payoffs}")

