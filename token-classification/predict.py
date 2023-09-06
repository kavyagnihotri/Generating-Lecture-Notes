import torch
import os
import sys
from transformers import AutoTokenizer, AutoModelForTokenClassification

MAX_SEQUENECE_LENGTH = 512                  # Adjusted as per the model's maximum token limit

def model_path(element):
    """
        Returns the path to the model directory. 
        Assumes the model is as follows "../models/{element}-location"
    """
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(curr_dir)
    model_dir = os.path.join(parent_dir, 'models', element + '-location')
    return model_dir


def load_model(model_dir):
    """
        Loads the finetuned model and tokenizer from the given directory.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    return tokenizer, model


def predict_location(text, tokenizer, model, output_file):
    """
        Predicts the location of the given text and writes the output to file.
    """
    # Subtract 2 for [CLS] and [SEP] tokens  
    # [SEP] is a separator token 
    # [CLS] is a token that will be used to predict whether or not Part B is a sentence that directly follows Part A.
    with open(output_file + '.txt', 'w') as f:
        for i in range(0, len(text), MAX_SEQUENECE_LENGTH - 2):  
            chunk = text[i:i + MAX_SEQUENECE_LENGTH - 2]
            input_ids = tokenizer.encode(chunk, add_special_tokens=True, truncation=True, padding=True)
            
            with torch.no_grad():
                outputs = model(torch.tensor(input_ids).unsqueeze(0))
            predictions = outputs.logits.argmax(dim=-1)[0]
            
            # Map label class indexes to string labels.
            tokens = tokenizer.convert_ids_to_tokens(input_ids)

            for token, pred in zip(tokens, predictions):
                f.write(token + ': ' + model.config.id2label[pred.item()] + '\n')
                # print(token, ': ', model.config.id2label[pred.item()])

        
def main():
    if len(sys.argv) < 4:
        print("Usage: python predict.py <element> <input_file>.txt <output_file>.txt")
        print("Hint: element is either 'image', 'pseudo-code' or 'formula'")
        sys.exit(1)
    
    element = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(input_file + '.txt', 'r') as f:
        text = f.read()

    model_dir = model_path(element)
    tokenizer, model = load_model(model_dir)
    predict_location(text, tokenizer, model, output_file)


if __name__ == '__main__':
    main()

# max_seq_length = 512  # Adjust this based on your model's maximum token limit
# tokenized_texts = []
# for i in range(0, len(text), max_seq_length - 2):             # Subtract 2 for [CLS] and [SEP] tokens
#     chunk = text[i:i + max_seq_length - 2]
#     input_ids = torch.tensor(tokenizer.encode(chunk)).unsqueeze(0)
#     with torch.no_grad():
#         outputs = model(input_ids)
#     predictions = outputs[0].argmax(axis=-1)[0][1:-1]         # Rid of [CLS] and [SEP] tokens (first and last)

#     for token, pred in zip(tokenizer.tokenize(text), predictions):
#         print(token, ': ', model.config.id2label[pred.numpy().item()])
