import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

def get_user_topic():
    topic = input('What topic do you want a text file about? \n')
    return topic.strip()

def generate_prompt(topic):
    return f"""
Write a well-structured text about the topic: {topic}
Structure it as follows:
- Heading (the topic as a title)
- Introduction (short paragraph)
- Main Content (use bullet points for key facts or details)
- Conclusion (short summary)
- Sources and References (list any sources, e.g., Wikipedia, at the end)
"""

def query_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    try:
        response.raise_for_status()
        result = response.json()
        # Extract the generated text
        return result['candidates'][0]['content']['parts'][0]['text']
    except (requests.exceptions.HTTPError, KeyError, IndexError) as e:
        print("[Gemini API Error]:", response.text)
        return f"[Error: Could not parse Gemini response: {e}]"

def save_to_file(topic, text):
    folder = os.path.join(os.path.dirname(__file__), 'topics')
    os.makedirs(folder, exist_ok=True)
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_', '-')).rstrip()
    filename = os.path.join(folder, f"{safe_topic}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved to {filename}")

def main():
    topic = get_user_topic()
    prompt = generate_prompt(topic)
    print("\nGenerating content using Gemini...\n")
    text = query_gemini(prompt)
    print(text)
    save_to_file(topic, text)

if __name__ == "__main__":
    main() 