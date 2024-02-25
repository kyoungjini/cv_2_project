import csv

f = open('urls.csv', 'r')
products = list(csv.reader(f))

up = []
down = []
other = []
unclassified = []

up_label = ['jacket', 'cardigan', 'shirts', 'knit', 'blouson', 'coat', 'mtm', 'mustang', 'sleeves', 'padding', 'blazer', 'zip-up', 'jumper', 'kara', 'sleeveless', 'vest', 'hood', 'wind', 'jacekt', '%EC%85%94%EC%B8%A0', '%EB%A7%A8%ED%88%AC%EB%A7%A8', '%ED%8B%B0', '%ED%9B%84%EB%93%9C', 'ma']
down_label = ['pants', 'slacks', '%EC%8A%AC%EB%9E%99%EC%8A%A4', '%ED%8C%AC%EC%B8%A0', 'pans', 'jean']
other_label = ['belt', 'muffler', 'boots', 'necklace', 'sneakers', 'ring', 'bracelet', 'sandal', 'glass', 'mule', 'bag', 'shoes', 'cap', 'flip-flop', 'slipper', 'loafer']

for n, shopping_url in products:
    # name = shopping_url[shopping_url.find('product/')+8:]
    # name = name[:name.find('/')]
    # print(name)
    name = shopping_url
    classified = False
    
    for l in up_label:
        if l in name:
            up.append(name)
            classified = True
            break
    
    for l in down_label:
        if l in name:
            down.append(name)
            classified = True
            break
        
    for l in other_label:
        if l in name:
            other.append(name)
            classified = True
            break
    
    if not classified: unclassified.append(name)
    
print(f'up: {len(up)}')
print(f'down: {len(down)}')
print(f'other: {len(other)}')