import torch
import os
import sys
from transformers import AutoTokenizer, AutoModelForTokenClassification
import jsonlines

MAX_SEQUENECE_LENGTH = 512                  # Adjusted as per the model's maximum token limit

def model_path(element, additional_path_sig):
    """
        Returns the path to the model directory. 
        Assumes the model is as follows "../models/{element}-location{-additional}"
    """
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(curr_dir)
    model_dir = os.path.join(parent_dir, 'models', element + '-location')
    if additional_path_sig is not None and additional_path_sig != '':
        model_dir = os.path.join(parent_dir, 'models', element + '-location-' + additional_path_sig)
    return model_dir


def load_model(model_dir):
    """
        Loads the finetuned model and tokenizer from the given directory.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    return tokenizer, model


# def predict_location(text, tokenizer, model, output_file):
#     """
#         Predicts the location of the given text and writes the output to file.
#     """
    
#     # with open(output_file, 'a') as f:
#     for i in range(0, len(text), MAX_SEQUENECE_LENGTH - 2):  
#         chunk = text[i:i + MAX_SEQUENECE_LENGTH - 2]
#         input_ids = tokenizer.encode(chunk, add_special_tokens=True, truncation=True, padding=True)
            
#         with torch.no_grad():
#             outputs = model(torch.tensor(input_ids).unsqueeze(0))
#         predictions = outputs.logits.argmax(dim=-1)[0]
            
#             # Map label class indexes to string labels.
#         tokens = tokenizer.convert_ids_to_tokens(input_ids)

#             # for token, pred in zip(tokens, predictions):
#             #     f.write(token + ': ' + model.config.id2label[pred.item()] + '\n')
#         json_data = {
#             "tokens": tokens,
#             "tags": [model.config.id2label[pred] for pred in predictions]
#         }
#         return json_data

def predict_location(text, tokenizer, model, output_file):
    for i in range(0, len(text), MAX_SEQUENECE_LENGTH - 2):
        chunk = text[i:i + MAX_SEQUENECE_LENGTH - 2]
        input_ids = tokenizer.encode(chunk, add_special_tokens=True, truncation=True, padding=True)

        with torch.no_grad():
            outputs = model(torch.tensor(input_ids).unsqueeze(0))
        predictions = outputs.logits.argmax(dim=-1)[0]

        tokens = tokenizer.convert_ids_to_tokens(input_ids)

        # Map label class indexes to string labels.
        tags = []
        for pred in predictions:
            pred_label = model.config.id2label.get(pred.item())
            if pred_label is not None:
                tags.append(pred_label)
            else:
                # Handle unknown labels here by assigning a default value or skipping
                tags.append("O")

        json_data = {
            "tokens": tokens,
            "tags": tags
        }
        return json_data



        
def main():
    if len(sys.argv) < 4:
        print("Usage: python predict.py <element> <input_file>.txt <output_file>.txt <additional_path_sig>")
        print("Hint: element is either 'image', 'formula', 'pseudocode' or 'pseudo-code'")
        print("Hint: additional_path_sig can be 'new', 'lda', etc")
        sys.exit(1)
    
    element = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    additional_path_sig = sys.argv[4]

    model_dir = model_path(element, additional_path_sig)
    tokenizer, model = load_model(model_dir)

    with open(input_file, 'r') as f, jsonlines.open(output_file, 'w') as f_out:
        # text = f.read()
        for line in f:
            line = line.strip()
            if line:
                result = predict_location(line, tokenizer, model, output_file)
                f_out.write(result)
    # predict_location(text, tokenizer, model, output_file)


if __name__ == '__main__':
    main()
