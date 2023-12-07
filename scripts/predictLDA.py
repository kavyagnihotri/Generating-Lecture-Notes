import gensim
from gensim import corpora
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import sys
import csv

def main():
    if len(sys.argv) != 3:
        print("Usage: python predictLDA.py <element> <input-file> ")
        print("The element can be either 'formula', 'image' or 'psuedocode'")
        print("The input should be a csv file containing the data, e.g. 'test.csv' or 'train.csv'")
        sys.exit(1)
    
    element = sys.argv[1]
    name = sys.argv[2]
    input_file = "./prompts/" + element + "/" + name
    output_file = "./prompts/" + element + "/predict_" + name.split('.')[0] + ".csv"

    df = pd.read_csv(input_file) 

    # Extract text data from the first column
    documents = df.iloc[:, 0].tolist()

    # Text Preprocessing
    stop_words = ['frac', 'displaystyl', 'textstyl', 'the', 'displaystyle', 'textstyle', 'mathbf', 'mathcal', 'mathbb', 'mathfrak', 'mathscr', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds', 'mathfrak', 'mathsf', 'mathtt', 'mathrm', 'mathit', 'mathnormal', 'mathbbm', 'mathds']
    lemmatizer = WordNetLemmatizer()

    tokenized_documents = [word_tokenize(doc.lower()) for doc in documents]
    filtered_documents = [
        [lemmatizer.lemmatize(word) for word in doc if word.isalnum() and word not in stop_words]
        for doc in tokenized_documents
    ]

    # Create Dictionary and Corpus
    dictionary = corpora.Dictionary(filtered_documents)
    corpus = [dictionary.doc2bow(doc) for doc in filtered_documents]

    # Train LDA Model
    num_topics = 20
    lda_model = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    # print the 20 topics along with their keywords
    topics_file = "./prompts/" + element + "/predict_topics_" + name.split('.')[0] + ".txt"
    for idx, topic in lda_model.print_topics(-1):
        with open(topics_file, "a") as file:
            file.write(f"Topic {idx}: {topic}\n\n")


    # Open the output file in append mode
    with open(output_file, "a", newline="") as file:
        writer = csv.writer(file)

        # Write the header if the file is empty
        if file.tell() == 0:
            header = ['text_index', 'predicted_topic']
            writer.writerow(header)

        # Classify each document
        for index, doc in enumerate(documents):
            tokenized_new_doc = [
                lemmatizer.lemmatize(word)
                for word in word_tokenize(doc.lower())
                if word.isalnum() and word not in stop_words
            ]
            bow_vector = dictionary.doc2bow(tokenized_new_doc)
            lda_result = lda_model[bow_vector]

            predicted_topic = max(lda_result, key=lambda x: x[1])[0]
            writer.writerow([index + 1, predicted_topic])

    print("Done " + element + " " + name)

if __name__ == "__main__":
    main()