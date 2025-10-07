sum = 0
with open(file='prices.txt', encoding='utf-8') as prices:
    for line in prices:
        l = line.removesuffix('\n').split('\t')
        sum += int(l[1])*int(l[2])
print(sum)