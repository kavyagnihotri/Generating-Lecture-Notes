# doesn't work, need to fix

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import csv

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name)
labels = ["Scientific", "Technical", "Other"]

def classify_entity(entity):
    # Tokenize the entity and prepare input for the model
    inputs = tokenizer(entity, return_tensors="pt", padding=True, truncation=True)
    
    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Interpret predictions
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).tolist()[0]
    predicted_label_idx = torch.argmax(logits, dim=1).item()
    predicted_label = labels[predicted_label_idx]
    
    with open('./csv_files/wikiEntities_classified.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([entity, predicted_label]) 
    
    print(f"Entity: {entity}")
    # print("Predicted Label:", predicted_label)
    # print("Label Probabilities:", dict(zip(labels, probabilities)))

def get_entities():
    with open('./csv_files/wikiEntities.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        return [row[0] for row in reader]
        

def main():
    entities = get_entities()
    for entity in entities:
        classify_entity(entity)
