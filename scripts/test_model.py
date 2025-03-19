from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch


# Load trained model
model_path = "app/models/testgen_llm"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Test input
user_story = "The system shall control the pump to deliver the calculated dose of insulin to the user. 4 The system shall ensure that the pump delivers the correct amount of insulin in response to the controller’s signals."
inputs = tokenizer(user_story, return_tensors="pt", truncation=True, padding="max_length")

with torch.no_grad():
    output = model.generate(**inputs)

generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated Test Case:", generated_text)
