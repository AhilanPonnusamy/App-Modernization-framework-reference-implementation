import sys
import requests


def query_vllm(prompt, llm_url):
    """Send a prompt to the vLLM server and return the response."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
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


def process_orm_entity(orm_entity_code, llm_url):
    """Generate a Quarkus REST API based on the provided ORM entity."""
    if not orm_entity_code.strip():
        return "ERROR: ORM entity input is empty."

    prompt = (
        f"Analyze the following Quarkus ORM entity code that uses Panache, and generate a complete REST API code for it. "
        f"Include all CRUD operations and finder methods for each field in the entity. Please do not produce boiler template or sample code and produce workable code. Use this example as a guide:\n\n"
        f"import java.util.List;\n"
        f"import javax.transaction.Transactional;\n"
        f"import javax.ws.rs.*;\n"
        f"import javax.ws.rs.core.MediaType;\n"
        f"import javax.ws.rs.core.Response;\n\n"
        f"import io.quarkus.panache.common.Sort;\n\n"
        f"@Path(\"/owners\")\n"
        f"@Consumes(MediaType.APPLICATION_JSON)\n"
        f"@Produces(MediaType.APPLICATION_JSON)\n"
        f"public class OwnerResource {{\n\n"
        f"    // Get all owners\n"
        f"    @GET\n"
        f"    public List<Owner> getAllOwners() {{\n"
        f"        return Owner.findAll(Sort.ascending(\"lastName\")).list();\n"
        f"    }}\n\n"
        f"    // Get owner by ID\n"
        f"    @GET\n"
        f"    @Path(\"/{{id}}\")\n"
        f"    public Owner getOwnerById(@PathParam(\"id\") Long id) {{\n"
        f"        return Owner.findById(id);\n"
        f"    }}\n\n"
        f"    // Get owners by first name\n"
        f"    @GET\n"
        f"    @Path(\"/search/firstName/{{firstName}}\")\n"
        f"    public List<Owner> getOwnersByFirstName(@PathParam(\"firstName\") String firstName) {{\n"
        f"        return Owner.list(\"firstName\", firstName);\n"
        f"    }}\n\n"
        f"    // Other CRUD operations...\n"
        f"}}\n\n"
        f"Here is the ORM entity code:\n\n{orm_entity_code}"
    )


    response = query_vllm(prompt, llm_url)
    return response


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_api_from_orm.py '<ORM_ENTITY_CODE>' <LLM_URL>")
        sys.exit(1)

    orm_entity_code = sys.argv[1]
    llm_url = sys.argv[2]

    if not orm_entity_code.strip():
        print("ERROR: ORM entity code input is empty.")
        sys.exit(1)

    print("Processing ORM Entity Code...")
    result = process_orm_entity(orm_entity_code, llm_url)
    print("\nGenerated Quarkus REST API Code:")
    print(result)


if __name__ == "__main__":
    main()
