import csv
import json
import sys

def read_csv_keys(csv_file):
    keys = set()
    with open(csv_file, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            keys.update(row)
    return keys

def filter_json(json_data, keys_to_include):
    return {key: json_data[key] for key in keys_to_include if key in json_data}

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python filter.py <csv_file>.csv <json_file>.json")
        sys.exit(1)

    csv_file = sys.argv[1]
    json_file = sys.argv[2]

    csv_keys = read_csv_keys(csv_file)
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    filtered_json = filter_json(json_data, csv_keys)

    output_json_file = json_file.replace('.json', '_filtered.json')
    with open(output_json_file, 'w') as file:
        json.dump(filtered_json, file, indent=4)

    print(f"Filtered JSON saved to '{output_json_file}'.")
