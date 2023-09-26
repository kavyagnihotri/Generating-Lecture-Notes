import ast
import json
import sys

def convert(input_file, output_file):

    # Read the text from the file
    with open(input_file, 'r') as file:
        input_text = file.read()

    # Convert the text to a dictionary using ast.literal_eval
    # This assumes the text in the file is in a valid Python dictionary format
    data_dict = ast.literal_eval(input_text)

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data_dict, indent=4)

    # Write the JSON string to a new file
    with open(output_file, 'w') as json_file:
        json_file.write(json_data)

    print("Conversion complete. JSON data has been saved to 'output.json'.")


if __name__ == "__main__":

    # Check that the user has provided the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python convert_to_json.py <input_file>.txt <output_file>.json")
        sys.exit(1)

    # Get the input and output file paths from the command line
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert(input_file, output_file)


