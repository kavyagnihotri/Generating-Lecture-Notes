import json
import os

def check_jsonline_sizes(file_path):
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            try:
                data = json.loads(line)
                words = data.get("tokens", [])
                tags = data.get("tags", [])
                
                if len(words) != len(tags):
                    print(f"Line {line_num}: Size mismatch - tokens: {len(words)}, tags: {len(tags)}")
            except json.JSONDecodeError:
                print(f"Line {line_num}: JSON decoding error")

if __name__ == "__main__":
    base_dir = "/Users/kavyagnihotri/Documents/personal/acads/4-1/generating-lecture-notes/prajna-project/json_files/"
    files = ["train.json", "test.json", "validation.json"]

    for file in files:
        print(f"Checking {file}")
        full_path = os.path.join(base_dir, file)
        check_jsonline_sizes(full_path)
        print("Done")
