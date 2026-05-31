import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

def generate_content(client: genai.Client, messages: list[types.Content]):
    return client.models.generate_content(model="gemini-2.5-flash", contents = messages)


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Api-key not found")
    
    print("Hello from your ai-cli-agent!")

    parser = argparse.ArgumentParser(description="Ai-cli-agent")
    parser.add_argument("cli_prompt", type=str, help="the user prompt")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.cli_prompt)])
    ]
    client = genai.Client(api_key=api_key)

    response = generate_content(client, messages)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:" + response.text)

if __name__ == "__main__":
    main()
