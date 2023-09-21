import json
import sys

def remove_for_tokens(data, mark):
    new_tokens = []
    new_tags = []
    
    for token, tag in zip(data['tokens'], data['tags']):
        if token != mark:
            new_tokens.append(token)
            new_tags.append(tag)
    
    data['tokens'] = new_tokens
    data['tags'] = new_tags
    if len(new_tokens) != len(new_tags):
        print("Error: len(new_tokens) != len(new_tags)")
    return data

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python remove_mark.py <mark> <input_file>.json")
        print("Mark can be FOR, IMG or PRE")
        sys.exit(1)

    print(sys.argv)
    mark = "$" + sys.argv[1] + "$"
    input_file = sys.argv[2]
    input_file_path = ""
    output_file_path = ""

    if mark == "$FOR$":
        input_file_path = "../data/formula-location-old/" + input_file
        output_file_path = "../data/formula-location/" + input_file
    elif mark == "$IMG$":
        input_file_path = "../data/image-location-old/" + input_file
        output_file_path = "../data/image-location/" + input_file
    elif mark == "$PRE$":
        input_file_path = "../data/pseudo-code-location-old/" + input_file
        output_file_path = "../data/pseudo-code-location/" + input_file


    # Read input file and process each line
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            json_data = json.loads(line)
            json_data = remove_for_tokens(json_data, mark)
            output_file.write(json.dumps(json_data) + '\n')
