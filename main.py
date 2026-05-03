import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

def main():
    parser = argparse.ArgumentParser(description="AI Toybot")
    parser.add_argument("user_prompt", type=str, help="Please enter valid prompt.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None: 
        raise RuntimeError("Environment variable not found.")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model = "gemini-2.5-flash", 
            contents = messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0)
        )
        for candidate in response.candidates:
            messages.append(candidate.content)

        usage = response.usage_metadata
        if usage is None:
            raise RuntimeError("Gemini API response failed")
    
        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if function_call_result.parts == []:
                    raise Exception(f"parts list is empty")
                if function_call_result.parts[0].function_response == None:
                    raise Exception(f"function_response is None")
                if function_call_result.parts[0].function_response.response == None: 
                    raise Exception(f"function_response.response is None")
                function_results.append(function_call_result.parts[0])
                if args.verbose: 
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else: 
            print("Response:")
            print(response.text)
            return
        
    print("Maximum number of iterations reached")
    sys.exit(1)

if __name__ == "__main__":
    main()
