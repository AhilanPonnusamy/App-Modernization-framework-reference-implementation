import sys
import requests


def query_vllm(prompt, llm_url):
    """Send a prompt to the vLLM server and return the response."""
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
        print(f"Error communicating with vLLM server: {e}")
        return "ERROR: Failed to fetch response"


def process_requirements_input(requirements_text, llm_url):
    """Process the requirements text to generate Hibernate ORM code."""
    if not requirements_text.strip():
        return "ERROR: Requirements input is empty."

    prompt = (
        f"Analyze the following table structure described in SQL, and generate Hibernate ORM entity classes with Panache ORM for Quarkus. Please generate classes for all tables. Use this sample code for formatting:\n\n"
        f"import javax.persistence.Column;\n"
        f"import javax.persistence.Entity;\n"
        f"import io.quarkus.hibernate.orm.panache.PanacheEntity;\n\n"
        f"@Entity\n"
        f"public class Person extends PanacheEntity {{\n"
        f"    @Column(name = \"first_name\")\n"
        f"    public String firstName;\n\n"
        f"    @Column(name = \"last_name\")\n"
        f"    public String lastName;\n\n"
        f"    public String salutation;\n"
        f"}}\n\n"
        f"Here is the table structure in SQL format:\n\n{requirements_text}"
    )

    response = query_vllm(prompt, llm_url)
    return response


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_orm.py '<SQL_TABLE_DEFINITION>' <LLM_URL>")
        sys.exit(1)

    sql_table_definition = sys.argv[1]
    llm_url = sys.argv[2]

    if not sql_table_definition.strip():
        print("ERROR: SQL table definition input is empty.")
        sys.exit(1)

    print("Processing SQL Table Definition...")
    result = process_requirements_input(sql_table_definition, llm_url)
    print("\nGenerated Hibernate ORM Code:")
    print(result)


if __name__ == "__main__":
    main()
