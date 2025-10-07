sum = 0
with open(file='text_file.txt', encoding='utf-8') as file:
    for line in file:
        line = line.removesuffix('\n').replace(' —', '').split(' ')
        sum += len(line)
print(sum)
