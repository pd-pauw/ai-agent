import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

def generate_content(client: genai.Client, messages: list[types.Content]):
    try:
        return client.models.generate_content(model="gemini-2.5-flash", contents = messages)
    except Exception as e :
        print(f"something went wrong calling gemini api: {e}")
        
def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Api-key not found")
    
    print("Hello from your ai-cli-agent!")

    parser = argparse.ArgumentParser(description="Ai-cli-agent")
    parser.add_argument("user_prompt", type=str, help="the user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt = args.user_prompt

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    client = genai.Client(api_key=api_key)

    response = generate_content(client, messages)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:" + response.text)

if __name__ == "__main__":
    main()
