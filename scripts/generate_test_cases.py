import openai
import os

# Set API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_test_case(story):
    """Generates a test case using OpenAI's GPT-3.5 Turbo"""
    prompt = f"Convert the following story into a Gherkin test case:\n\n{story}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response["choices"][0]["message"]["content"]

# Example usage
story = "As a user, I want to log in so that I can access my dashboard."
test_case = generate_test_case(story)
print(test_case)
