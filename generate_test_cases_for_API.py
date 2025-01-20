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


def process_api_code(api_code, llm_url):
    """Generate unit test cases for the provided API code."""
    if not api_code.strip():
        return "ERROR: API code input is empty."

    prompt = (
        f"Analyze the following Quarkus REST API code and generate comprehensive unit test cases using JUnit 5 and RestAssured. "
        f"Include tests for all CRUD operations and finder methods defined in the API. Use the following test case structure as a guide:\n\n"
        f"import io.quarkus.test.junit.QuarkusTest;\n"
        f"import io.restassured.RestAssured;\n"
        f"import io.restassured.http.ContentType;\n"
        f"import org.junit.jupiter.api.Test;\n\n"
        f"import javax.transaction.Transactional;\n"
        f"import java.util.HashMap;\n"
        f"import java.util.Map;\n\n"
        f"import static org.hamcrest.Matchers.*;\n\n"
        f"@QuarkusTest\n"
        f"public class OwnerResourceTest {{\n\n"
        f"    @Test\n"
        f"    public void testGetAllOwners() {{\n"
        f"        RestAssured.given()\n"
        f"                .when().get(\"/owners\")\n"
        f"                .then()\n"
        f"                .statusCode(200)\n"
        f"                .body(\"size()\", greaterThanOrEqualTo(0));\n"
        f"    }}\n\n"
        f"    @Test\n"
        f"    public void testGetOwnerById() {{\n"
        f"        RestAssured.given()\n"
        f"                .pathParam(\"id\", 1) // Assuming ID 1 exists\n"
        f"                .when().get(\"/owner/{{id}}\")\n"
        f"                .then()\n"
        f"                .statusCode(200)\n"
        f"                .body(\"id\", is(1));\n"
        f"    }}\n\n"
        f"    @Test\n"
        f"    @Transactional\n"
        f"    public void testCreateOwner() {{\n"
        f"        Map<String, Object> newOwner = new HashMap<>();\n"
        f"        newOwner.put(\"ownerId\", null); // ID should be auto-generated\n"
        f"        newOwner.put(\"firstName\", \"Jane\");\n"
        f"        newOwner.put(\"lastName\", \"Doe\");\n"
        f"        newOwner.put(\"address\", \"123 Elm Street\");\n"
        f"        newOwner.put(\"city\", \"Springfield\");\n"
        f"        newOwner.put(\"telephone\", \"555-1234\");\n\n"
        f"        RestAssured.given()\n"
        f"                .contentType(ContentType.JSON)\n"
        f"                .body(newOwner)\n"
        f"                .when().post(\"/owner\")\n"
        f"                .then()\n"
        f"                .statusCode(201)\n"
        f"                .body(\"firstName\", is(\"Jane\"))\n"
        f"                .body(\"lastName\", is(\"Doe\"));\n"
        f"    }}\n\n"
        f"    // Additional tests...\n"
        f"}}\n\n"
        f"Ensure the tests cover as many use cases and edge cases and validate HTTP status codes. Here is the API code:\n\n{api_code}"
    )

    response = query_vllm(prompt, llm_url)
    return response


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_test_cases_for_API.py '<API_CODE>' <LLM_URL>")
        sys.exit(1)

    api_code = sys.argv[1]
    llm_url = sys.argv[2]

    if not api_code.strip():
        print("ERROR: API code input is empty.")
        sys.exit(1)

    print("Processing API Code...")
    result = process_api_code(api_code, llm_url)
    print("\nGenerated Unit Test Cases:")
    print(result)


if __name__ == "__main__":
    main()
