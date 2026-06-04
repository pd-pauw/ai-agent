import os
import sys
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompt import system_prompt
from call_function import available_functions, call_function

def generate_content(client: genai.Client, messages: list[types.Content]):
    try:
        return client.models.generate_content(
            model="gemini-2.5-flash", 
            contents = messages, 
            config= types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt)
                )
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

    for _ in range(20):

        response = generate_content(client, messages)

        if not response.usage_metadata:
         raise RuntimeError("Gemini API response appears to be malformed")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if args.verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return

        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if ( not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                    or not function_call_result.parts[0].function_response.response
                ):
                    raise Exception(f"Error: Empty function response for {function_call.name}")
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_results.append(function_call_result.parts[0])
        messages.append(types.Content(role="user", parts=function_results))

    print("Model did not generate response in 20 loops")
    sys.exit(-1)

if __name__ == "__main__":
    main()
