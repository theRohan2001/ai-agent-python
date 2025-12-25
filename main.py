import os
import argparse
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="ai-agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))

function_results = []

if response.function_calls:
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)
        if not function_call_result.parts:
            raise Exception("call_function returned Content with no parts")
        if function_call_result.parts[0].function_response is None:
            raise Exception("Content.parts[0].function_response is None")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("FunctionResponse.response is None")
        
        function_results.append(function_call_result.parts[0])

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(f"Response: \n{response.text}")