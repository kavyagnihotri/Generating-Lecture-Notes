import torch
import os
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Directory
curr_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(curr_dir)
model_dir = os.path.join(parent_dir, 'models', 'image-location')

# Load model
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForTokenClassification.from_pretrained(model_dir)

# Take input
text = input("Enter text: ").strip()

max_seq_length = 512  # Adjust this based on your model's maximum token limit
tokenized_texts = []

for i in range(0, len(text), max_seq_length - 2):  # Subtract 2 for [CLS] and [SEP] tokens
    chunk = text[i:i + max_seq_length - 2]
    input_ids = tokenizer.encode(chunk, add_special_tokens=True, truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(torch.tensor(input_ids).unsqueeze(0))

    # Get the predicted labels for each token
    predictions = outputs.logits.argmax(dim=-1)[0]
    
    # Map label class indexes to string labels.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    for token, pred in zip(tokens, predictions):
        print(token, ': ', model.config.id2label[pred.item()])

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
