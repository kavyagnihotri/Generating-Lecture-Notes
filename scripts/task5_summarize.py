import csv
import re

# entity, more entities ... 
entityMap_adjList = {}

# entity, [first_hop_entities], [second_hop_entities]
entityMap_twoHops = {}

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
    for key in entityMap_adjList:
        first_hop = entityMap_adjList[key]
        second_hop = []
        for entity in first_hop:
            for e in entityMap_adjList[entity]:
                second_hop.append(e)
        
        second_hop = list(set(second_hop))
        entityMap_twoHops[key] = [first_hop, second_hop]


# Defining main function
def main():
    makeEntityAdjList()
    makeTwoHops()
      
if __name__=="__main__":
    main()