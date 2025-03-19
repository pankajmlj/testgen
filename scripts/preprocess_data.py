import pandas as pd
import json
from transformers import AutoTokenizer

# Load tokenizer
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load datasets
train_df = pd.read_csv("data/train_50.csv")
test_df = pd.read_csv("data/test_5.csv")

# Function to tokenize input and output
def preprocess_function(data):
    inputs = tokenizer(data["user_story"], truncation=True, padding="max_length", max_length=512)
    targets = tokenizer(data["test_case"], truncation=True, padding="max_length", max_length=512)
    return {"input_ids": inputs["input_ids"], "labels": targets["input_ids"]}

# Apply preprocessing and convert to DataFrame
train_tokenized = pd.DataFrame(train_df.apply(preprocess_function, axis=1).tolist())
test_tokenized = pd.DataFrame(test_df.apply(preprocess_function, axis=1).tolist())

# Save tokenized data as JSON
train_tokenized.to_json("data/train_preprocessed.json", orient="records", lines=True)
test_tokenized.to_json("data/test_preprocessed.json", orient="records", lines=True)

print("✅ Preprocessing complete. Tokenized data saved as JSON.")
