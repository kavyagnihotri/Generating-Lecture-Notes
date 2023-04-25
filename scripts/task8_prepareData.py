import os
import csv
import json

def removeNewLines(dataset_folder):
    output_folder = os.path.join(dataset_folder, "modified")
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(dataset_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(dataset_folder, filename), "r") as file:
                text = file.read()
            text = text.replace("\n", "\\n")
            with open(os.path.join(output_folder, filename), "w") as file:
                file.write(text)

def getEntityNames():
    entity_set = set()
    with open('./csv_files/wikiEntities.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) # Skip header row
        for row in csv_reader:
            entity_name = row[0]
            entity_set.add(entity_name)
    return

def readTextJson(dataset_folder, valid_entity_set):
    #  delimiter = ": '", in text files
    values = {}
    for filename in os.listdir(dataset_folder):
        if filename.endswith(".txt"):
            break


    
    

    

if __name__ == "__main__":
    dataset_folder = "./csv_files/bert_dataset_img/short/"
    # removeNewLines(dataset_folder)
    # modified_dataset_folder = os.path.join(dataset_folder, "modified")
    valid_entity_set = getEntityNames()