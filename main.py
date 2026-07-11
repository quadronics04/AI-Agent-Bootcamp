from dotenv import load_dotenv
import os
import time

from google import genai
from google.genai.errors import ServerError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)

# prompt = "What is Photosynthesis?"

# max_attempts = 4

# for attempt in range(max_attempts):
#     try:
#         response = client.models.generate_content(
#             model="gemini-3.1-flash-lite-preview",
#             contents=prompt
#         )

#         print(response.text)
#         break

#     except ServerError as error:
#         if attempt == max_attempts - 1:
#             print("Gemini is still busy. Please run the program again after some time.")
#             print(f"Technical error: {error}")
#         else:
#             wait_time = 2 ** attempt
#             print(f"Gemini is busy. Retrying in {wait_time} seconds...")
#             time.sleep(wait_time)

question = input("Ask Gemini: ")

response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview",
    contents=question
)
print("Thinking...\n")
print("\nGemini:\n")
print(response.text)
print("\nDone!")