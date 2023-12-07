import csv
import requests
from bs4 import BeautifulSoup

entityMap_adjList = {}              # entity, more entities ... 
entityMap_twoHops = {}              # entity, [first_hop_entities], [second_hop_entities]
entities = {}                       # entity, link

def makeEntityAdjList():
    entityMap_adjList.clear()
    with open('./csv_files/entity_map_complete.csv') as f:
        csv_file = csv.reader(f)

        # skips header
        next(csv_file)             
        for row in csv_file:
            key = row[0]
            
            # set
            entities = [] 
            for entity in row[1:]:
                entities.append(entity)

            entities = list(set(entities))
            entityMap_adjList[key] = entities

def makeTwoHops():
    makeEntityAdjList()
    for key in entityMap_adjList:
        first_hop = entityMap_adjList[key]
        second_hop = []
        for entity in first_hop:
            for e in entityMap_adjList[entity]:
                second_hop.append(e)
        
        second_hop = list(set(second_hop))
        entityMap_twoHops[key] = [first_hop, second_hop]

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

if __name__ == '__main__':
    makeTwoHops()
    makeEntityLinks()

    i = 0
    for entry in entityMap_twoHops:
        print(entry)
        print(getSummary(entry))
        first_hop = entityMap_twoHops[entry][0]
        second_hop = entityMap_twoHops[entry][1]
        first_hop_summaries = []
        second_hop_summaries = []

        for entity in first_hop:
            first_hop_summaries.append(getSummary(entity))

        for entity in second_hop:
            second_hop_summaries.append(getSummary(entity))

        print(str(first_hop_summaries))
        print(str(second_hop_summaries), end="\n\n")
        i += 1
        if i > 3:
            break
