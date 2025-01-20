import sys
import requests


def query_llm(prompt, llm_url):
    """Send a prompt to the LLM server and return the response."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "granite",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(llm_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip() if "choices" in response_data else "No response content received."
    except requests.RequestException as e:
        print(f"Error communicating with LLM server: {e}")
        return "ERROR: Failed to fetch response"


def generate_react_app_code(requirements, llm_url):
    """Generate a React application code based on user requirements."""
    if not requirements.strip():
        return "ERROR: Requirements input is empty."

    prompt = (
        f"Based on the following requirements, generate a complete React application code. "
        f"Include detailed code snippets for components, state management, and integration with backend APIs. "
        f"Focus on reusable components, Material-UI for UI components, filtering, sorting, and pagination. "
        f"Use React functional components and hooks where appropriate.\n\n"
        f"Requirements:\n\n{requirements}"
    )

    return query_llm(prompt, llm_url)


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_react_app_code.py '<REQUIREMENTS>' <LLM_URL>")
        sys.exit(1)

    requirements = sys.argv[1]
    llm_url = sys.argv[2]

    if not requirements.strip():
        print("ERROR: Requirements input is empty.")
        sys.exit(1)

    print("Processing requirements...")
    result = generate_react_app_code(requirements, llm_url)

    if result.startswith("ERROR"):
        print(result)
        sys.exit(1)

    print("\nGenerated React App Code:")
    print(result)


if __name__ == "__main__":
    main()
