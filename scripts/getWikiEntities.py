import csv
import requests
from bs4 import BeautifulSoup as bs

# path = '/Users/kavyagnihotri/Documents/personal/acads/prajna-project/wikiEntities.csv'
outputFile = open('wikiEntities.csv', 'w')
writer = csv.writer(outputFile)
header = ['entity_name', 'entity_URI']
writer.writerow(header)

with open('TeKnowbaseEntities.tsv') as f:
    tsv_file = csv.reader(f, delimiter="\t")
    next(tsv_file)                                            # skips header
    cnt = 0
    other = 0
    for row in tsv_file:
      if len(row) < 2:
         other += 1
         continue
      
      name,link = row
      if 'wikipedia' not in link:
        other += 1
        continue

      writer.writerow(row)
      cnt += 1

    # print(cnt)
    # print(other)
    # print(cnt+other)

outputFile.close()