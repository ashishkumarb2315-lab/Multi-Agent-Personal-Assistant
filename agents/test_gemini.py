import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)

response = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain artificial intelligence in one simple sentence."
)

print(response.output_text)