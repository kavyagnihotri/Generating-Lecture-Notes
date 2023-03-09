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

def writeToCSV():
    ''' Writes in the form [entity, string of hop1 entities, string of hop2 entities] '''
    outputFile = open('entity_with_twoHops.csv', 'w')
    writer = csv.writer(outputFile)
    header = ['entity_name', 'first_hop_entities', 'second_hop_entities']
    writer.writerow(header)
    
    for key in entityMap_twoHops:
        writer.writerow([key, entityMap_twoHops[key][0], entityMap_twoHops[key][1]])

# def extractFromCSV(entity):
#           DOES NOT WORK
#     with open('entity_with_twoHops.csv') as f:
#         csv_file = csv.reader(f)
#         next(csv_file)                       # skips header

#         for row in csv_file:
#             if entity is not row[0]:
#                 continue

#             hop1 = row[1][1:-1]
#             hop2 = row[2][1:-1]

#             hop1 = re.split(",| |'", hop1)
#             hop2 = re.split(",| |'", hop2)

# Defining main function
def main():
    makeEntityAdjList()
    makeTwoHops()
    # writeToCSV()            
      
if __name__=="__main__":
    main()