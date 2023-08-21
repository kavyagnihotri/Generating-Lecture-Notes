import requests
from bs4 import BeautifulSoup
import csv
import re
import json

# Token labels
B_IMG_LABEL = "B-IMG"
I_IMG_LABEL = "I-IMG"
O_LABEL = "O"
IMG_TAG = "$IMG$"

# Example Counts
TRAIN_EXAMPLE_COUNT = 50000
VALIDATION_EXAMPLE_COUNT = 12000
TEST_EXAMPLE_COUNT = 3000

def text_from_url(url):
    """
        Extract the text from the url
        Additions: Replace all the images with IMG_TAG token i.e. " $IMG$ "
    """
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    content_div = soup.find('div', {'class': 'mw-body-content'}) or soup.find('div', {'class': 'vector-body'})

    # Extract the text inside the content div
    text = ''
    for element in content_div.descendants:
        if element.name == 'img':
            text += " " + IMG_TAG + " "
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
    filtered_substrings = [sub for sub in substrings if any(IMG_TAG in word for word in sub)]
    return [' '.join(sub) for sub in filtered_substrings]


# def words_from_sentence(sentence):
#     """
#         Split the text into words. 
#         Additions: Split words like "Category$IMG$" into separate tokens of "Category" and "$IMG$"
#     """
#     words = sentence.split()

#     new_words = []
#     for word in words:
#         if word != IMG_TAG and IMG_TAG in word:
#             parts = word.split(IMG_TAG)
#             parts.append(IMG_TAG)
#             new_words.extend(part for part in parts if part != '')
#         else:
#             new_words.append(word)
#     return new_words
    

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
        prev_sentence = sentences[i - 1]
        prev_words = prev_sentence.split()
        curr_words = sentence.split()
        # prev_words = words_from_sentence(prev_sentence)
        # curr_words = words_from_sentence(sentence)

        if i > 0:
            if any(IMG_TAG in word for word in curr_words):
                # Annotate the words of the sentence JUST BEFORE $IMG$
                ner_labels = [B_IMG_LABEL] + [I_IMG_LABEL] * (len(prev_words) - 1)
            elif len(sentences) > 1 and i != len(sentences) - 1:
                ner_labels = [O_LABEL] * len(prev_words)
        
        words_array += prev_words
        ner_labels_array += ner_labels

        # There are more than one sentences and this is the last sentence
        if i == len(sentences) - 1:
            words_array += curr_words
            ner_labels_array += [B_IMG_LABEL if word == IMG_TAG else O_LABEL for word in curr_words]
    return words_array, ner_labels_array


# def is_invalid(ner_labels_array):
#     """
#         Returns true if there is no B-IMG label in the ner_labels_array
#     """
#     return B_IMG_LABEL not in ner_labels_array


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
    train_file = './json_files/train.json'                # 50,000 jsonlines
    validation_file = './json_files/validation.json'      # 12,000 jsonlines
    test_file = './json_files/test.json'                  # 3,000 jsonlines

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