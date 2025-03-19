# TestGen-LLM

TestGen-LLM is an AI-driven test case generator that converts Jira user stories into structured BDD (Gherkin) test cases.


# TestGen-LLM: Automated Test Case Generation

## Overview
TestGen-LLM is an AI-powered system that generates test cases from user stories. It supports:
- Generating test cases from direct user input.
- Fetching Jira issue descriptions and converting them into test cases.
- Posting generated test cases as Jira comments.
- Option to use OpenAI's GPT model or a trained T5 model.

## Features
- **REST API using FastAPI**
- **Integration with Jira API**
- **Environment variable-based configuration**
- **Option to choose between OpenAI GPT-3.5 and a local T5 model**

## Installation
### Prerequisites
- Python 3.8+
- `pip` installed
- OpenAI API key
- Jira API token

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/testgen-llm.git
   cd testgen-llm
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export JIRA_EMAIL="your-email@example.com"
   export JIRA_API_TOKEN="your-jira-api-token"
   export JIRA_BASE_URL="https://your-jira-instance.atlassian.net/rest/api/2/issue/"
   ```
   Or add them to `~/.zshrc` for persistence:
   ```bash
   echo 'export OPENAI_API_KEY="your-openai-api-key"' >> ~/.zshrc
   echo 'export JIRA_EMAIL="your-email@example.com"' >> ~/.zshrc
   echo 'export JIRA_API_TOKEN="your-jira-api-token"' >> ~/.zshrc
   echo 'export JIRA_BASE_URL="https://your-jira-instance.atlassian.net/rest/api/2/issue/"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints
### 1️⃣ Generate Test Case from User Story
**POST /generate**
```bash
curl -X POST "http://127.0.0.1:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"user_story": "As a user, I want to reset my password.", "use_gpt": true}'
```

### 2️⃣ Generate Test Case from Jira Issue
**POST /generate-with-jira**
```bash
curl -X POST "http://127.0.0.1:8000/generate-with-jira" \
     -H "Content-Type: application/json" \
     -d '{"jira_id": "SCRUM-123", "use_gpt": false}'
```


## 🚀 Features
- ✅ Automates test case generation
- ✅ Uses Hugging Face’s Transformers
- ✅ Deployable via FastAPI and Kubernetes

## 📂 Project Structure
```
TestGen-LLM/
│── app/                            # FastAPI Service
│   ├── models/                    # Trained model directory
│   ├── main.py                     # API Endpoint for inference
│── data/                           
│   ├── train.csv                    # Training data
│   ├── test.csv                     # Test data
│── scripts/                         
│   ├── train_model.py               # Model training script
│   ├── preprocess_data.py           # Data preprocessing script
│── deployment/                      
│   ├── Dockerfile                   # Dockerfile for containerization
│   ├── requirements.txt              # Dependencies
│   ├── testgen-llm-deployment.yaml   # Kubernetes Deployment config
│   ├── testgen-llm-service.yaml      # Kubernetes Service config
│── .gitignore                        
│── README.md                        
```

## 🛠 Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/your-repo/testgen-llm.git
   cd testgen-llm
   ```

2. **Install dependencies:**
   ```bash
   pip install -r deployment/requirements.txt
   ```

3. **Preprocess data:**
   ```bash
   python scripts/preprocess_data.py
   ```

4. **Train the model:**
   ```bash
   python scripts/train_model.py
   ```

5. **Run the API locally:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 🐳 Docker Setup

1. **Build the Docker image:**
   ```bash
   docker build -t testgen-llm .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 testgen-llm
   ```

## ☁️ Kubernetes Deployment

1. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f deployment/testgen-llm-deployment.yaml
   kubectl apply -f deployment/testgen-llm-service.yaml
   ```

2. **Check service:**
   ```bash
   kubectl get svc
   ```

## 🔥 API Usage
Once the API is running, test it with:
```bash
curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d '{"user_story": "As a user, I want to log in so that I can access my dashboard."}'
```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints
### 1️⃣ Generate Test Case from User Story
**POST /generate**
```bash
curl -X POST "http://127.0.0.1:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"user_story": "As a user, I want to reset my password.", "use_gpt": true}'
```

### 2️⃣ Generate Test Case from Jira Issue
**POST /generate-with-jira**
```bash
curl -X POST "http://127.0.0.1:8000/generate-with-jira" \
     -H "Content-Type: application/json" \
     -d '{"jira_id": "SCRUM-123", "use_gpt": false}'
```
