import json
import csv
import sys
import os

# formula -> [1479, 348, 943, 250, 536, 850, 338, 157, 1716, 230, 655, 298, 314, 264, 421, 204, 321, 1105, 497, 815]
# image -> [1377, 1915, 1944, 7502, 90, 1976, 336, 570, 1241, 361, 839, 149, 2089, 2330, 1075, 166, 608, 730, 306, 658]
# pseudocode -> [228, 593, 379, 256, 715, 118, 337, 86, 453, 488, 116, 591, 237, 322, 97, 123, 1662, 513, 172, 1281]
# Define maximum entries for each topic in train and test sets
entries = [228, 593, 379, 256, 715, 118, 337, 86, 453, 488, 116, 591, 237, 322, 97, 123, 1662, 513, 172, 1281]
max_train_entries = [min(350, int(0.8 * entry)) for entry in entries]
max_test_entries = [min(150, int(0.2 * entry)) for entry in entries]

max_train_entries[2] = 0
max_test_entries[2] = 0

max_train_entries[13] = 0
max_test_entries[13] = 0

# Read the JSON lines file
def read_json_lines(file_name):
    with open(file_name, 'r') as file:
        data = [json.loads(line) for line in file]
    return data

def main():
    if len(sys.argv) != 2:
        print('Usage: python make_sets.py element>')
        sys.exit(1)
    element = sys.argv[1]
    csv_location = os.path.join('.', 'prompts', element, 'predict_all.csv')

    predicted_topics = {}
    with open(csv_location, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            predicted_topics[int(row['text_index']) - 1] = row['predicted_topic']

    print(entries, max_train_entries, max_test_entries)
    
    # Initialize dictionaries to store train and test data for each topic
    train_data = {str(topic): [] for topic in range(20)}
    test_data = {str(topic): [] for topic in range(20)}

    # Read the entire JSON lines file
    json_location = os.path.join('.', 'prompts', element, 'all.json')
    all_data = read_json_lines(json_location)

    # Count the entries for each topic in train and test sets
    train_count = {str(topic): 0 for topic in range(20)}
    test_count = {str(topic): 0 for topic in range(20)}

    # Filter the data based on the required number of entries for each topic
    # csv is one indexed, json is zero indexed
    for index, entry in enumerate(all_data):
        if index < len(predicted_topics):
            predicted_topic = predicted_topics[index] # Adjust for 1-indexing
            topic_index = int(predicted_topic)
            if train_count[predicted_topic] < max_train_entries[topic_index]:
                train_data[predicted_topic].append(entry)
                train_count[predicted_topic] += 1
            elif test_count[predicted_topic] < max_test_entries[topic_index]:
                test_data[predicted_topic].append(entry)
                test_count[predicted_topic] += 1

    json_location = os.path.join('.', 'prompts', element, 'train.json')
    with open(json_location, 'w') as train_file:
        for _, data in train_data.items():
            for entry in data:
                train_file.write(json.dumps(entry) + '\n')

    json_location = os.path.join('.', 'prompts', element, 'test.json')
    with open(json_location, 'w') as test_file:
        for _, data in test_data.items():
            for entry in data:
                test_file.write(json.dumps(entry) + '\n')

if __name__ == '__main__':
    main()