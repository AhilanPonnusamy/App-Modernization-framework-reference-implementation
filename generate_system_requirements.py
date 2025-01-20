import os
import sys

def consolidate_files_by_tag(input_folder, tag_name):
    """
    Consolidates content from all files starting with the given tag name followed by '::'.
    Returns the consolidated content as a string.
    """
    # Ensure the input folder exists
    if not os.path.isdir(input_folder):
        raise FileNotFoundError(f"The input folder '{input_folder}' does not exist.")

    consolidated_content = []

    # Iterate through files in the input folder
    current_tag_name = ""
    for file_name in os.listdir(input_folder):
        if file_name.startswith(f"{tag_name}::") or tag_name.startswith("<ALL>"):
            file_path = os.path.join(input_folder, file_name)
            if os.path.isfile(file_path):
                try:
                    # Read file contents
                    with open(file_path, "r", encoding="utf-8") as file:
                        if current_tag_name != tag_name:
                            current_tag_name = file_name.split("::")[0]
                            consolidated_content.append(current_tag_name)   
                            consolidated_content.append("\n")
                            consolidated_content.append("-" * 50 + "\n")
                         
                        consolidated_content.append(file.read())
                except Exception as e:
                    print(f"Error reading file '{file_path}': {e}")

    # Format the consolidated content
    #result = f"{tag_name}\n"
    #result += "-" * 50 + "\n"  # Optional separator
    result = "".join(consolidated_content)

    return result


if __name__ == "__main__":
    # Ensure the script receives two arguments
    if len(sys.argv) != 3:
        print("Usage: python consolidate_by_tag.py <input_folder> <tag_name>")
        sys.exit(1)

    # Parse command-line arguments
    input_folder = sys.argv[1]
    tag_name = sys.argv[2]
    tag_name = tag_name.strip().upper()    # Remove leading and trailing whitespace.

    try:
        consolidated_content = consolidate_files_by_tag(input_folder, tag_name)
        #print("Consolidated Content:")
        print(consolidated_content)
    except Exception as e:
        print(f"Error: {e}")
