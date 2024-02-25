import csv

f = csv.reader(open('urls.csv', 'r'))

urls = set()

for index, position, url in f:
    urls.add(url)

print(len(urls))