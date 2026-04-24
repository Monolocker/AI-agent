import argparse
import os
from dotenv import load_dotenv
from google import genai

def main():
    parser = argparse.ArgumentParser(description="AI Toybot")
    parser.add_argument("user_prompt", type=str, help="Please enter valid prompt.")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None: 
        raise RuntimeError("Environment variable not found.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = args.user_prompt
    )


    if response.usage_metadata is None:
        raise RuntimeError("Gemini API response failed")
    
    usage = response.usage_metadata

    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
