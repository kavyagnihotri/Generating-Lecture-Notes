from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch
import os
import sys

def load_model(finetuned_model):
    # Load the fine-tuned model and tokenizer
    current_script_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(os.path.dirname(current_script_path))
    model_name = parent_dir + '/models/' + finetuned_model
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return model, tokenizer

def predict(model, tokenizer, input_text):
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model(**inputs)
    predicted_labels = torch.argmax(outputs.logits, dim=2)
    predicted_tags = [tokenizer.convert_ids_to_tokens(tag_id) for tag_id in predicted_labels[0]]
    return predicted_tags

def main():
    if len(sys.argv) < 2:
        print("Usage: python predict.py finetuned_model_name")
        print("Hint: finetuned_model_name is either 'image-location', 'pseudo-code-location' or 'formula-location'")
        sys.exit(1)
    
    finetuned_model = sys.argv[1]
    model, tokenizer = load_model(finetuned_model)

    print("Put your input text here: ")
    input_text = input().strip()
    predicted_tags = predict(model, tokenizer, input_text)
    print(predicted_tags)

if __name__ == "__main__":
    main()  
