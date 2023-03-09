import csv

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

            entities = set(entities)
            entityMap_adjList[key] = list(entities)

makeEntityAdjList()
# for entry in entityMap_adjList:
#     print(entry, entityMap_adjList[entry])


# CHECK


def makeTwoHops():
    for key in entityMap_adjList:
        first_hop = entityMap_adjList[key]
        second_hop = []
        for entity in first_hop:
            mapping = entityMap_adjList[entity]
            for e in mapping:
                second_hop.append(e)

        second_hop = set(second_hop)
        entityMap_twoHops[key] = [first_hop, list(second_hop)]
        print(entityMap_twoHops)

makeTwoHops()

# def writeToCSV():
#     outputFile = open('entity_with_twoHops.csv', 'w')
#     writer = csv.writer(outputFile)
#     header = ['entity_name', 'first_hop_entities', 'second_hop_entities']
#     writer.writerow(header)

#     row = []
#     i = 0
#     for key in entityMap_twoHops:
#         first_hop = entityMap_twoHops[key][0]
#         second_hop = entityMap_twoHops[key][1]
#         row = [key, first_hop, second_hop]
#         print(row)

#         break

# writeToCSV()