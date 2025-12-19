import os
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="ai-agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()


response = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)
if response.usage_metadata:
    prompt_token = response.usage_metadata.prompt_token_count
    response_token = response.usage_metadata.candidates_token_count
else:
    raise RuntimeError("No response from the model")

print(f"User prompt: {args.user_prompt}")
print(f"Prompt tokens: {prompt_token}")
print(f"Response tokens: {response_token}")
print(f"Response: \n{response.text}")