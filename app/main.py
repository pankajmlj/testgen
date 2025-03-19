import os
import torch
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import openai

app = FastAPI()

# Load trained model
model_path = "app/models/testgen_llm"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Set OpenAI API Key (Ensure it's set as an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Jira API Configuration
JIRA_BASE_URL = "https://wilp-team-w1988001.atlassian.net/rest/api/2/issue/"
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {"Content-Type": "application/json"}

class StoryInput(BaseModel):
    user_story: str
    use_gpt: bool

class JiraTestCaseRequest(BaseModel):
    jira_id: str
    use_gpt: bool

def generate_test_case_gpt(story):
    """Generates a test case using OpenAI's GPT-3.5 Turbo"""
    prompt = f"Convert the following story into a Gherkin test case:\n\n{story}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response["choices"][0]["message"]["content"]

@app.post("/generate")
def generate_test_case(data: StoryInput):
    if not data.user_story.strip():
        raise HTTPException(status_code=400, detail="User story cannot be empty.")
    
    if data.use_gpt:
        return {"test_case": generate_test_case_gpt(data.user_story)}
    else:
        inputs = tokenizer(data.user_story, return_tensors="pt", truncation=True, padding="max_length")
        with torch.no_grad():
            output = model.generate(**inputs)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return {"test_case": generated_text}

@app.post("/generate-with-jira")
def generate_test_case_from_jira(data: JiraTestCaseRequest):
    response = requests.get(f"{JIRA_BASE_URL}{data.jira_id}", auth=JIRA_AUTH, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Jira issue not found.")
    
    issue_data = response.json()
    user_story = issue_data.get("fields", {}).get("description", "")
    
    if not user_story:
        raise HTTPException(status_code=400, detail="Jira issue has no description.")
    
    if data.use_gpt:
        test_case = generate_test_case_gpt(user_story)
    else:
        inputs = tokenizer(user_story, return_tensors="pt", truncation=True, padding="max_length")
        with torch.no_grad():
            output = model.generate(**inputs)
        test_case = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Post comment to Jira
    comment_data = {
        "body": f"Generated Test Case:\n```gherkin\n{test_case}\n```"
    }
    comment_response = requests.post(
        f"{JIRA_BASE_URL}{data.jira_id}/comment", 
        auth=JIRA_AUTH, 
        headers=HEADERS, 
        json=comment_data
    )
    
    if comment_response.status_code not in [200, 201]:
        raise HTTPException(status_code=500, detail="Failed to post comment to Jira.")
    
    return {"jira_id": data.jira_id, "test_case": test_case}
