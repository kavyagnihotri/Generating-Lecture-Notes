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

def validJson(filename):
    print("here")
    valid_entity_set = getEntityNames()

    with open(filename, 'r', encoding="utf-8") as json_file:
        data = json.loads(json_file.read())    
        
        for entity_name in data:
            if entity_name not in valid_entity_set:
                print("Invalid entity: " + entity_name)
                return False

def read_files_and_process(filename):
    processed_lines = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        # processed_lines = []
        for line in lines:
            if "$IMG$" in line:
                word = line.strip().replace("$IMG$", "")
                processed_lines.append(f"{word} IMG IMG IMG\n")
            else:
                words = line.strip().split()
                for word in words:
                    processed_lines.append(f"{word} O O O\n")
        # result.append("".join(processed_lines))
        print(f"{processed_lines}")
    return processed_lines



if __name__ == "__main__":
    dataset_folder = "./pages"

    for filename in os.listdir(dataset_folder):
        if filename.endswith(".txt"):
            read_files_and_process(filename)
            # readJson(os.path.join(dataset_folder, filename))
