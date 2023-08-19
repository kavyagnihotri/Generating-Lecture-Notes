import requests
from bs4 import BeautifulSoup
import csv
import re
import json


def text_from_url(url):
    """
        Extract the text from the url
    """
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    content_div = soup.find('div', {'class': 'mw-body-content'}) or soup.find('div', {'class': 'vector-body'})

    # Extract the text inside the content div
    text = ''
    for element in content_div.descendants:
        if element.name == 'img':
            text += "$IMG$"
        else:
            if hasattr(element, 'get_text'):
                text += element.get_text(separator=' ')
    return text


def clean_text(text):
    """
        Clean the text by removing all the special characters(except '.', '?', '!') and extra whitespaces
    """
    pattern = r'[^a-zA-Z0-9\s.!?$IMG$]'                     # pattern to keep only alphanumeric characters and ending punctuations
    cleaned_text = re.sub(pattern, '', text)
    cleaned_text = ' '.join(cleaned_text.strip().split())   # remove extra whitespaces
    return cleaned_text


def split_and_filter_text(text, word_limit=700):
    """
    Split the text into smaller parts of word_limit words
    """
    words = text.split()
    substrings = [words[i:i + word_limit] for i in range(0, len(words), word_limit)]
    filtered_substrings = [sub for sub in substrings if any("$IMG$" in word for word in sub)]
    return [' '.join(sub) for sub in filtered_substrings]


def annotate_part(part):
    """
        Annotate the text with the labels.
        Returns two arrays: words_array and it's corresponding ner_labels_array
    """
    B_IMG_LABEL = "B-IMG"
    I_IMG_LABEL = "I-IMG"
    O_LABEL = "O"

    words_array = []
    ner_labels_array = []

    sentences = re.split(r'\s*[.!?]\s*', part)  # Split by sentence-ending punctuations
    for i, sentence in enumerate(sentences):
        prev_sentence = sentences[i - 1]
        words = prev_sentence.split()

        if "$IMG$" in sentence and i > 0:
            # Annotate the words of the sentence JUST BEFORE $IMG$
            ner_labels = [B_IMG_LABEL] + [I_IMG_LABEL] * (len(words) - 1)
        else:
            ner_labels = [O_LABEL] * len(words)
        
        words_array += words
        ner_labels_array += ner_labels

        if i == len(sentences) - 1:
            words = sentence.split()
            ner_labels = [O_LABEL] * len(words) # current sentence's ner labels
            words_array += words
            ner_labels_array += ner_labels
    return words_array, ner_labels_array


def write_to_jsonl(output_file, annotated_array):
    """
    Append word_array and tag_array as JSON objects to a JSONLines file
    """
    word_array, tag_array = annotated_array
    assert len(word_array) == len(tag_array), "word_array and tag_array must have the same length"
    
    with open(output_file, 'a') as file:
        entry = { "tokens": word_array, "tags": tag_array }
        json.dump(entry, file)
        file.write('\n')


def main():
    input_file = './csv_files/wikiEntities_mini.csv'
    train_file = './csv_files/train.csv'                # 50,000 jsonlines
    validation_file = './csv_files/validation.csv'      # 12,000 jsonlines
    test_file = './csv_files/test.csv'                  # 3,000 jsonlines

    example_count = 0

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for _, url in reader:
            text = text_from_url(url)
            cleaned_text = clean_text(text)
            filtered_parts = split_and_filter_text(cleaned_text)
            annotated_arrays = [annotate_part(part) for part in filtered_parts]

            if example_count < 50000:
                output_filename = train_file
            elif example_count < 62000:
                output_filename = validation_file
            elif example_count < 65000:
                output_filename = test_file
            else:
                break

            for annotated_array in annotated_arrays:
                write_to_jsonl(output_filename, annotated_array)
                example_count += 1
            
            print(example_count)

if __name__ == '__main__':
    

    main()


