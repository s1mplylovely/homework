with open(file='source.txt', encoding='utf-8') as source:
    with open(file='destination.txt', mode='w', encoding='utf-8') as dest:
        for line in source:
            dest.write(f"{line}")
