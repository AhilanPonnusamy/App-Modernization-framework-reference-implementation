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


def generate_data_model(file_path, llm_url):
    """Generate a data model based on the requirements file."""
    try:
        with open(file_path, "r") as file:
            requirements_content = file.read()

        if not requirements_content.strip():
            print(f"The file '{file_path}' is empty.")
            return

        prompt = (
            f"Analyze the following requirements and generate a data model "
            f"in the form of an entity-relationship diagram description (tables, fields, types, and relationships):\n\n{requirements_content}"
        )

        data_model = query_vllm(prompt, llm_url)

        if "ERROR" in data_model:
            print(f"Failed to generate data model for '{file_path}'.")
        else:
            print("\nGenerated Data Model:")
            print(data_model)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_sql_script(file_path, llm_url):
    """Generate an SQL script based on the requirements file."""
    try:
        with open(file_path, "r") as file:
            requirements_content = file.read()

        if not requirements_content.strip():
            print(f"The file '{file_path}' is empty.")
            return

        prompt = (
            f"Analyze the following requirements and generate an SQL script "
            f"that creates the necessary tables and relationships based on the data model implied by the requirements:\n\n{requirements_content}"
        )

        sql_script = query_vllm(prompt, llm_url)

        if "ERROR" in sql_script:
            print(f"Failed to generate SQL script for '{file_path}'.")
        else:
            print("\nGenerated SQL Script:")
            print(sql_script)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_artifacts.py <file_path> <llm_url>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    llm_url = sys.argv[2]

    if not file_path.is_file():
        print(f"The specified path is not a file: {file_path}")
        sys.exit(1)

    print(f"Processing file: {file_path}")
    print("Generating Data Model...")
    generate_data_model(file_path, llm_url)
    print("\nGenerating SQL Script...")
    generate_sql_script(file_path, llm_url)


if __name__ == "__main__":
    main()
