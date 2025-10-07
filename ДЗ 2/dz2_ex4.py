d = {}
with open(file='input.txt', encoding='utf-8') as inp:
    with open(file='unuque_output.txt', mode='w', encoding='utf-8') as outp:
        for line in inp:
            d[line.removesuffix('\n')] = 1
        for key in d.keys():
            outp.write(f'{key+'\n'}')
