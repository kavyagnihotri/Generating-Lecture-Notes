import numpy as np
import lda
import pandas as pd
import sys
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk

# def setup():
#     nltk.download('omw-1.4')
#     nltk.download('stopwords')
#     nltk.download('wordnet')

def preprocess_document(text):
    words = text.split()
        
    # Initialize the NLTK stemmer and lemmatizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    # Apply stemming, lemmatization, and stopword removal
    processed_words = []
    # stop_words = set(stopwords.words("english"))
    extra_words = ['X', 'displaystyl', 'textstyl']
    for word in words:
        word = stemmer.stem(word)  # Stemming
        word = lemmatizer.lemmatize(word)  # Lemmatization
        if word not in extra_words:  # Stopword removal
            processed_words.append(word)
    
    return ' '.join(processed_words)

def main():
    # setup()
    if len(sys.argv) != 3:
        print("Usage: python LDAtopic.py <element> <input-file> > <output-file>")
        print("The element can be either 'formula', 'image' or 'psuedocode'")
        print("The input should be a csv file containing the data, e.g. 'test.csv' or 'train.csv'")
        print("The output file is be a csv file with the given name")
        return
    
    element = sys.argv[1]
    file = sys.argv[2]
    location = "./prompts/" + element + "/" + file
    
    # Load the TSV file into a Pandas DataFrame
    entries = []

    with open(location, "r") as file:
        for line in file:
            parts = line.strip().split('\t')
            entry = {"document_text": parts[0]}
            entries.append(entry)

    df = pd.DataFrame(entries)

    # Apply the preprocessing function to the "document text" column
    df["new_document_text"] = df["document_text"].apply(preprocess_document)

    # Extract the document text column
    documents = df["new_document_text"]

    # Create a Count vectorizer
    vectorizer = CountVectorizer()

    # Fit and transform the documents to create the document-term matrix
    dtm = vectorizer.fit_transform(documents)

    # Convert the document-term matrix to a Pandas DataFrame for easier handling
    dtm_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names_out())

    X = dtm_df.to_numpy()

    vocab = np.array(vectorizer.get_feature_names_out())

    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(X)
    topic_word = model.topic_word_
    n_top_words = 10
    for i, topic_dist in enumerate(topic_word):
        topic_words = vocab[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_
    for i in range(len(df)):
        print("{} (top topic: {})".format(df.iloc[i, 0], doc_topic[i].argmax()))

if __name__ == "__main__":
    main()