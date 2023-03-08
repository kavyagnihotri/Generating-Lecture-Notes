# from = tree_structure
# to = history_of_ibm

import csv
import requests
from bs4 import BeautifulSoup

entities = {}
# link, name
with open('wikiEntities.csv') as f:
    csv_file = csv.reader(f)
    next(csv_file)          # skips header
    for name, link in csv_file:
        entities[link] = name


outputFile = open('entity_map-7001.csv', 'w')
writer = csv.writer(outputFile)
header = ['entity_name']
writer.writerow(header)

# outputFile2 = open('entity_unknown_map.csv', 'w')
# writer2 = csv.writer(outputFile2)
# writer2.writerow(header)

with open('wikiEntities-begin-7001.csv') as f:
    csv_file = csv.reader(f)
    next(csv_file)                       # skips header

    for name, link in csv_file:
        res = requests.get(url=link)
        soup = BeautifulSoup(res.content, 'html.parser')

        row = []
        row.append(name)

        # row2 = []
        # row2.append(name)

        # Give location where text is stored which you wish to alter
        unordered_list = soup.find("div", {"class": "mw-parser-output"})

        # Find children of an element
        children = unordered_list.findChildren()

        cnt = 0
        seenH2 = False
        edges = []

        # Print all children of an element
        for child in children:
            # child = str(child)
            if "<h2" == (str(child))[0:3]:
                break

            if "<p>" == (str(child))[0:3]:
                cnt += 1
                if seenH2 == False and cnt > 5:
                    break
                a_tags = child.find_all('a')

                if len(a_tags) == 0:
                    continue
                # print("here")
                for a in a_tags:
                    href = a.get("href")

                    if not href:
                        continue
                    
                    if '/wiki' == href[0:5]:
                        edge = "https://en.wikipedia.org" + href
                        edges.append(edge)
                        # row2.append(edge)
                        
                        if edge in entities:
                            row.append(entities[edge])

                        # find the href in the list you have
                        # if present append to the row
        print(row)
        writer.writerow(row)
        # writer2.writerow(row2)

outputFile.close()
