import os
import sys
from pathlib import Path
import requests


def query_vllm(prompt, llm_url):
    """Send a prompt to the vLLM server and return the response."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",  # Model name for vLLM
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(llm_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the response text
        return response_data["choices"][0]["message"]["content"].strip() if "choices" in response_data else "No response content received."
    except requests.RequestException as e:
        print(f"Error communicating with vLLM server: {e}")
        return "ERROR: Failed to fetch response"


def generate_requirements(file_path, llm_url):
    """Generate high-level requirements for the source code in the file."""
    try:
        with open(file_path, "r") as file:
            code_content = file.read()

        if not code_content.strip():
            print(f"The file '{file_path}' is empty.")
            return

        # Determine the programming language based on file extension
        extension = file_path.suffix.lower()
        if extension == ".java":
            language = "Java"
        elif extension in [".js", ".ts"]:
            language = "JavaScript/TypeScript"
        elif extension == ".cs":
            language = "C# (.NET)"
        elif extension == ".html":
            language = "HTML"
        else:
            print(f"Unsupported file type: {extension}")
            return

        prompt = (
            f"Analyze the following {language} code and generate high-level requirements one requirement per line with - at the begining in the format 'The system shall xxxx':\n\n{code_content}"
        )

        requirements = query_vllm(prompt, llm_url)

        if "ERROR" in requirements:
            print(f"Failed to generate requirements for '{file_path}'.")
        else:
            #print(f"High-level requirements for '{file_path}':\n")
            print(requirements)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_requirements.py <file_path> <llm_url>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    llm_url = sys.argv[2]

    if not file_path.is_file():
        print(f"The specified path is not a file: {file_path}")
        sys.exit(1)

    generate_requirements(file_path, llm_url)


if __name__ == "__main__":
    main()
