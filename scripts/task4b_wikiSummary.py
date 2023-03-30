import csv
import requests
from bs4 import BeautifulSoup

entities = {}                       # entity, link

def makeEntityLinks():
    with open('./csv_files/wikiEntities.csv') as f:
        csv_file = csv.reader(f)
        
        # skips header
        next(csv_file)         

        for name, link in csv_file:
            entities[name] = link

def getSummary(entity):
    link = entities[entity]
    simpleLink = "https://simple" + link[10:]

    res = requests.get(url=simpleLink) 
    if res.status_code != 200:
        res = requests.get(url=link)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    unordered_list = soup.find("div", {"class": "mw-parser-output"})

    children = unordered_list.findChildren()
    cnt = 0
    seenH2 = False
    text = ""

    for child in children:
        if "<h2" == (str(child))[0:3]:
            break

        if "<p>" == (str(child))[0:3]:
            cnt += 1
            if seenH2 == False and cnt > 3:
                break
            text += child.getText()
            
    return text

def generateSummaryCSV(): 
    makeEntityLinks()
    outputFile = open('./csv_files/entity_summary.csv', 'w')
    writer = csv.writer(outputFile)
    header = ['entity_name', 'summary']
    writer.writerow(header)

    for entity in entities:
        row = []
        row.append(entity)
        row.append(getSummary(entity))
        writer.writerow(row)

    outputFile.close()

if __name__ == '__main__':
    generateSummaryCSV()
