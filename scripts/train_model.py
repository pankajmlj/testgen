import os
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset

# Load tokenizer and model
# model_name = "t5-small"
model_name = "facebook/bart-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Function to load NDJSON correctly
def load_ndjson(filename):
    with open(filename, "r") as f:
        return [json.loads(line) for line in f]

# Load preprocessed JSON data (NDJSON format)
train_data = load_ndjson("data/train_preprocessed.json")
test_data = load_ndjson("data/test_preprocessed.json")

# Convert JSON data to Hugging Face Dataset
train_dataset = Dataset.from_dict({
    "input_ids": [d["input_ids"] for d in train_data], 
    "labels": [d["labels"] for d in train_data]
})
test_dataset = Dataset.from_dict({
    "input_ids": [d["input_ids"] for d in test_data], 
    "labels": [d["labels"] for d in test_data]
})

# Training arguments with checkpoints enabled
training_args = TrainingArguments(
    output_dir="app/models/testgen_llm",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="epoch",  # Ensures evaluation & saving happens every epoch
    save_strategy="epoch",  # Saves model after each epoch
    save_total_limit=2,  # Keeps only the last 2 checkpoints
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,  # Loads best checkpoint
    save_steps=500,  # Save checkpoint every 500 steps (adjust as needed)
    evaluation_strategy="epoch",
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()

# Ensure model directory exists before saving
save_path = "app/models/testgen_llm"
os.makedirs(save_path, exist_ok=True)

# Save model checkpoint explicitly
print("🔹 Saving model checkpoint...")
trainer.save_model(save_path)

# Explicitly save model & tokenizer
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

# Check if `pytorch_model.bin` was saved
if os.path.exists(os.path.join(save_path, "pytorch_model.bin")):
    print("✅ Model successfully saved: pytorch_model.bin exists")
else:
    print("❌ Model save failed: pytorch_model.bin is missing")

print("✅ Model training complete. Model saved to", save_path)
