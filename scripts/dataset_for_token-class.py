import requests
from bs4 import BeautifulSoup
import csv
import re
import json

# Token labels
B_LABEL = "B-LOC"
I_LABEL = "I-LOC"
O_LABEL = "O"
ELEMENT_TAG = "$IMG$"

# Example Counts
TRAIN_EXAMPLE_COUNT = 25000
VALIDATION_EXAMPLE_COUNT = 6000
TEST_EXAMPLE_COUNT = 1500

def text_from_url(url):
    """
        Extract the text from the url
        Additions: Replace all the images with ELEMENT_TAG token
    """
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    content_div = soup.find('div', {'class': 'mw-body-content'}) or soup.find('div', {'class': 'vector-body'})

    # Extract the text inside the content div
    text = ''
    for element in content_div.descendants:
        if element.name == 'img':
            text += " " + ELEMENT_TAG + " "
        else:
            if hasattr(element, 'get_text'):
                text += element.get_text(separator=' ')
    return text


def clean_text(text):
    """
        Clean the text by removing all the special characters(except '.', '?', '!') and extra whitespaces
    """
    # pattern = r'[^a-zA-Z0-9\s.!?$IMG$]'                               # pattern to keep only alphanumeric characters and ending punctuations
    pattern = r'[^a-zA-Z0-9\s.!?{}]'.format(re.escape(ELEMENT_TAG))     # pattern to keep only alphanumeric characters and ending punctuations
    cleaned_text = re.sub(pattern, '', text)
    cleaned_text = ' '.join(cleaned_text.strip().split())                # remove extra whitespaces
    return cleaned_text


def split_and_filter_text(text, word_limit=700):
    """
    Split the text into smaller parts of word_limit words
    """
    words = text.split()
    substrings = [words[i:i + word_limit] for i in range(0, len(words), word_limit)]
    filtered_substrings = [sub for sub in substrings if any(ELEMENT_TAG in word for word in sub)]
    return [' '.join(sub) for sub in filtered_substrings]


def annotate_part(part):
    """
        Annotate the text with the labels.
        Returns two arrays: words_array and it's corresponding ner_labels_array
    """
    words_array = []
    ner_labels_array = []

    # Split by sentence-ending punctuations
    sentences = re.split(r'\s*[.!?]\s*', part)  
    for i, sentence in enumerate(sentences):
        prev_words = sentences[i - 1].split()
        curr_words = sentence.split()
        ner_labels = []

        if any(word == ELEMENT_TAG for word in curr_words) and i > 0:
            # Annotate the words of the previous sentence JUST BEFORE $IMG$
            ner_labels = [B_LABEL] + [I_LABEL] * (len(prev_words) - 1)
        else:
            ner_labels = [O_LABEL] * len(prev_words)
        
        words_array += prev_words
        ner_labels_array += ner_labels

        # There are more than one sentences and this is the last sentence
        if len(sentences) > 1 and i == len(sentences) - 1:
            words_array += curr_words
            ner_labels_array += [B_LABEL if word == ELEMENT_TAG else O_LABEL for word in curr_words]
    return words_array, ner_labels_array


def write_to_jsonl(output_file, annotated_array):
    """
    Append word_array and tag_array as JSON objects to a JSONLines file
    """
    words_array, ner_labels_array = annotated_array
    # assert len(words_array) == len(ner_labels_array), "words_array and ner_labels_array must have the same length"
    if len(words_array) != len(ner_labels_array):
        print("Warning: word_array and ner_labels_array must have the same length. Skipping this entry.")
        # continue
    
    with open(output_file, 'a') as file:
        entry = { "tokens": words_array, "tags": ner_labels_array }
        json.dump(entry, file)
        file.write('\n')


def main():
    input_file = './csv_files/wikiEntities.csv'
    train_file = './json_files/train-1.json'                # 25,000 jsonlines
    validation_file = './json_files/validation-1.json'      # 6,000 jsonlines
    test_file = './json_files/test-1.json'                  # 1,500 jsonlines

    example_count = 0

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for _, url in reader:
            text = text_from_url(url)
            cleaned_text = clean_text(text)
            filtered_parts = split_and_filter_text(cleaned_text)
            annotated_arrays = [annotate_part(part) for part in filtered_parts]

            if example_count < TRAIN_EXAMPLE_COUNT:
                output_filename = train_file
            elif example_count < TRAIN_EXAMPLE_COUNT + VALIDATION_EXAMPLE_COUNT:
                output_filename = validation_file
            elif example_count < TRAIN_EXAMPLE_COUNT + VALIDATION_EXAMPLE_COUNT + TEST_EXAMPLE_COUNT:
                output_filename = test_file
            else:
                break

            for annotated_array in annotated_arrays:
                write_to_jsonl(output_filename, annotated_array)
                example_count += 1
            
            print(example_count)
            

if __name__ == '__main__':
    main()