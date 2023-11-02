from transformers import DistilBertTokenizer, DistilBertModel
import torch
import torch.nn as nn

# Load pre-trained DistilBERT model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertModel.from_pretrained(model_name)
num_categories = 12

classification_head = nn.Linear(model.config.dim, num_categories)  

# Example input text
# input_text = "commutative_(terms_relating_to_algorithms_and_data_structures) : In mathematics, a binary operation is commutative if changing the order of the operands does not change the result.It is a fundamental property of many binary operations, and many mathematical proofs depend on it.Most familiar as the name of the property that says something like \"3 + 4 = 4 + 3\" or \"2 \u00d7 5 = 5 \u00d7 2\", the property can also be used in more advanced settings.The name is needed because there are operations, such as  division and subtraction, that do not have it (for example, \"3 \u2212 5 \u2260 5 \u2212 3\"); such operations are not commutative, and so are referred to as noncommutative operations.The idea that simple operations, such as the multiplication and addition of numbers, are commutative was for many years implicitly assumed."
input_text = "There are a variety of legal types of organizations, including corporations, governments, non-governmental organizations, political organizations, international organizations, armed forces, charities, not-for-profit corporations, partnerships, cooperatives, and educational institutions, etc."

input_ids = tokenizer(input_text, return_tensors="pt")["input_ids"]
features = model(input_ids).last_hidden_state

# Apply classification head
logits = classification_head(features[:, 0, :])
probabilities = torch.softmax(logits, dim=1)
predicted_category = torch.argmax(probabilities, dim=1).item()

category_labels = ["history", "computer science", "people", "physics", "mathematics", "chemistry", "religion", "biology", "geography", "book", "engineering", "organization"]
predicted_category_label = category_labels[predicted_category]
print(predicted_category_label)