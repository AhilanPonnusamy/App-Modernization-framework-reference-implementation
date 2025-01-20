import os
import streamlit as st
import json
import subprocess

# Function to build the directory tree recursively
def build_directory_tree(path):
    """Recursively builds a nested dictionary representing the directory tree."""
    tree = {}
    for root, dirs, files in os.walk(path):
        parts = os.path.relpath(root, path).split(os.sep)
        current_level = tree
        for part in parts:
            current_level = current_level.setdefault(part, {})
        current_level["__files__"] = sorted(files)
    return tree

# Recursive function to display the folder structure
def display_tree(tree, base_path="", level=0):
    """Recursively displays the directory tree with proper nesting and styles."""
    for key, value in tree.items():
        if key == "__files__":
            for file in value:
                file_path = os.path.join(base_path, file)
                if st.session_state.selected_file == file_path:
                    selected_style = "background-color: #f0f0f0; font-weight: bold;"
                else:
                    selected_style = ""
                if st.sidebar.button(
                    f"{'&nbsp;&nbsp;' * (level * 4)}📄 {file}",
                    key=file_path,
                    help=f"Click to view {file}",
                ):
                    st.session_state.selected_file = file_path
                    st.session_state.generated_requirements = ""  # Clear when switching files
                    st.session_state.requirement_file_exist = False
                    st.session_state.requirement_file_name = ""

                    if requirements_exist(file_path):
                        st.session_state.generated_requirements = read_requirements(file_path)
                        st.session_state.requirement_file_exist = True
        else:
            st.sidebar.markdown(
                f"<div style='margin-left: {level * 20}px; color: yellow; padding: 5px; font-weight: bold;'>📁 {key}</div>",
                unsafe_allow_html=True,
            )
            display_tree(value, os.path.join(base_path, key), level + 1)

# Function to check if requirements already exist for a file
def requirements_exist(file_path):
    folder_name = os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    full_file_name = find_file_with_pattern("./requirements",f"{folder_name}-{file_name}-requirements.txt")
    if full_file_name is not None:
      requirements_file = os.path.join(full_file_name)
      st.session_state.requirement_file_name = requirements_file
    #requirements_file = os.path.join("requirements", f"{folder_name}-{file_name}-requirements.txt")
      return os.path.exists(requirements_file)
    else:
        return None

# Function to read requirements file contents
def read_requirements(file_path):
    folder_name = os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    full_file_name = find_file_with_pattern("./requirements",f"{folder_name}-{file_name}-requirements.txt")
    if full_file_name is not None:
      requirements_file = os.path.join(full_file_name)
    return read_file(requirements_file)

def find_file_with_pattern(folder_name, file_name):
    try:
        for entry in os.listdir(folder_name):
            if "::" in entry and entry.split("::", 1)[1] == file_name:
                return os.path.join(folder_name, entry)
        return None  # No matching file found
    except Exception as e:
        return f"Error: {e}"

# Function to read file contents
def read_file(file_path):
    """Reads and displays the contents of the file."""
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

# Function to run the `generate_requirements.py` script
def generate_requirements(file_path, llm_url):
    """Runs the generate_requirements.py script and returns its output."""
    try:
        result = subprocess.run(
            ["python", "generate_requirements.py", file_path, llm_url],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error generating requirements: {e.stderr}"
    
# Function to run the `generate_datamodel_and_sql.py` script
def generate_datamodel_and_sql(file_path, llm_url):
    """Runs the generate_requirements.py script and returns its output."""
    try:
        result = subprocess.run(
            ["python", "generate_datamodel_and_sql.py", file_path, llm_url],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error generating requirements: {e.stderr}"
    
# Function to run the `generate_orm_objects.py` script    
def generate_orm_objects(datamodel, llm_url):
    """Runs the generate_orm_objects.py script and returns its output."""
    try:
        result = subprocess.run(
            ["python", "generate_orm_objects.py", datamodel, llm_url],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error generating requirements: {e.stderr}"
    
# Function to run the `generate_api_form_orm_object.py` script    
def generate_API(ormcode, llm_url):
    """Runs the generate_orm_objects.py script and returns its output."""
    try:
        result = subprocess.run(
            ["python", "generate_api_from_orm_object.py", ormcode, llm_url],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error generating requirements: {e.stderr}"
    
# Function to run the `generate_test_cases_for_API.py` script    
def generate_test_cases(APIcode, llm_url):
    """Runs the generate_test_cases_for_API.py script and returns its output."""
    try:
        result = subprocess.run(
            ["python", "generate_test_cases_for_API.py", APIcode, llm_url],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error generating requirements: {e.stderr}"

# Function to run the `generate_react_ui_for_requirements.py` script    
def generate_ui(requirements, llm_url):
    """Runs the generate_react_ui_for_requirements.py script and returns its output."""
    try:
        result = subprocess.run(
            ["python", "generate_react_ui_for_requirements.py", requirements, llm_url],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error generating requirements: {e.stderr}"

# Function to run 'generate_system_requirements.py' script
def generate_system_requirements(folder_path, tag_name):
    """Runs the generate_requirements.py script and returns its output."""
    try:
        result = subprocess.run(
            ["python", "generate_system_requirements.py", folder_path, tag_name],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error generating requirements: {e.stderr}"

# Function to save requirements to a file
def save_requirements(content, selected_file, selected_option):
    """Saves the requirements content to a file in the requirements folder."""
    folder_name = os.path.basename(os.path.dirname(selected_file))
    file_name = os.path.basename(selected_file)
    requirements_folder = "requirements"
    os.makedirs(requirements_folder, exist_ok=True)
    if selected_option == "Enter new tag...":
        tag = "UNGROUPED"
    else:
        tag = selected_option.upper()
    requirements_folder = "requirements"
    folder_name = os.path.basename(os.path.dirname(selected_file))
    if st.session_state.requirement_file_name == "":
        output_file = os.path.join(requirements_folder, f"{tag}::{folder_name}-{file_name}-requirements.txt")
    else:
        output_file = st.session_state.requirement_file_name
    
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(content)
        return f"Requirements saved successfully to {output_file}"
    except Exception as e:
        return f"Error saving requirements: {e}"

# Function to list all generated requirements files
def list_generated_files():
    """Lists all saved requirement files from the 'requirements' folder."""
    requirements_folder = "requirements"
    if not os.path.exists(requirements_folder):
        return []
    return sorted(os.listdir(requirements_folder))

# Function to list all generated system/functional requirements files
def list_generated_system_requirement_files():
    """Lists all saved requirement files from the 'requirements' folder."""
    requirements_folder = "requirements/system_requirements"
    if not os.path.exists(requirements_folder):
        return []
    return sorted(os.listdir(requirements_folder))

# Path to the groupings.json file
GROUPINGS_FILE = "groupings.json"

# Function to load options from groupings.json
def load_groupings():
    """Loads groupings from the JSON file or returns an empty list if the file doesn't exist."""
    if os.path.exists(GROUPINGS_FILE):
        with open(GROUPINGS_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                st.error("Error reading groupings.json. The file might be corrupted.")
                return []
    return []


def save_grouping(option):
    """Saves a new grouping option to the JSON file."""
    # Ensure the parent directory exists
    directory = os.path.dirname(GROUPINGS_FILE)
    if directory:  # Only create directory if one is specified
        os.makedirs(directory, exist_ok=True)

    # Load existing groupings or create a new list
    groupings = []
    if os.path.exists(GROUPINGS_FILE):
        with open(GROUPINGS_FILE, "r", encoding="utf-8") as file:
            groupings = json.load(file)

    # Add the new option if it doesn't already exist
    if option not in groupings:
        groupings.append(option.upper())
        with open(GROUPINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(groupings, file, indent=4)
        return True
    return False


# Streamlit App Layout
st.set_page_config(layout="wide")
st.title("📂 AI App Modernization Assistant ...")

# Sidebar for project info and folder selection
st.sidebar.title("📂 Project Info")
selected_folder = st.sidebar.text_input("Enter project folder path:")

# Initialize session state variables
if "folder_tree" not in st.session_state:
    st.session_state["folder_tree"] = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None
if "generated_requirements" not in st.session_state:
    st.session_state.generated_requirements = ""
if "selected_generated_file" not in st.session_state:
    st.session_state.selected_generated_file = None
if "generated_files_content" not in st.session_state:
    st.session_state.generated_files_content = ""
if "requirement_file_exist" not in st.session_state:
    st.session_state.requirement_file_exist = False
if "requirement_file_name" not in st.session_state:
    st.session_state.requirement_file_name = ""
if "gen_content" not in st.session_state:
    st.session_state.gen_content = ""
if "show_contols" not in st.session_state:
    st.session_state.show_controls = False

# Load Project Structure button
if st.sidebar.button("Load Project Structure"):
    if selected_folder and os.path.isdir(selected_folder):
        st.session_state["folder_tree"] = build_directory_tree(selected_folder)
    else:
        st.sidebar.warning("Invalid folder path. Please enter a valid folder.")

# Display folder structure in the sidebar
if st.session_state["folder_tree"]:
    st.sidebar.markdown("### Folder Structure")
    display_tree(st.session_state["folder_tree"], base_path=selected_folder)

# Tabs
tabs = st.tabs(["File Workbench", "Generated Requirement Files","Functional Requirements Workbench","Modernization Workbench"])
llm_url = "http://localhost:8000/v1/chat/completions"
# Tab 1: File Workbench
with tabs[0]:
    st.subheader("📁 File Details")
    
    if st.session_state.selected_file:
        content = read_file(st.session_state.selected_file)
        
        # Display content in a text area
        st.text_area(
            f"Contents of {os.path.basename(st.session_state.selected_file)}", 
            content, 
            height=500, 
            key="file_content"
        )
        
        # Display the generated requirements if they exist
        if st.session_state.generated_requirements:
            st.subheader("Generated Requirements")

            # If the requirement file alredy exists then no need to retag it.
            if not st.session_state.requirement_file_exist:
                edited_content = st.text_area(
                    "Generated Requirements", 
                    st.session_state.generated_requirements, 
                    height=300, 
                    key="generated_requirements_box"
                )             
                # Load options from groupings.json
                options = load_groupings()

                # Add a placeholder for the "Enter new option" selection
                options_with_placeholder = options + ["Enter new module name..."]
                # Create a dropdown
                selected_option = st.selectbox("Select a module name/tag for this requiremnt file:", options_with_placeholder)
                # Handle new option input
                if selected_option == "Enter new module name...":
                    new_option = st.text_input("Enter a new module name:")
                    if new_option:
                        if save_grouping(new_option):
                            st.success(f"New option '{new_option}' added successfully!")
                            st.experimental_rerun()  # Reload the app to update the dropdown options
                        else:
                            st.warning(f"Option '{new_option}' already exists.")
                else:
                    st.write(f"Selected Tag: {selected_option}")

                # If the file doesn't exist and no options yet, notify the user
                if not options and not os.path.exists(GROUPINGS_FILE):
                    st.info("The groupings.json file does not exist yet. Add your first option to create it.")
                else:
                    st.markdown("<div style='text-align: center; color: gray;'>Select a file to view its contents.</div>", unsafe_allow_html=True)
            
                # Add a Save Requirements button
                if st.button("Save Requirements"):
                    save_message = save_requirements(edited_content, st.session_state.selected_file,selected_option)
                    st.success(save_message)
            else:
                edited_content = st.text_area(
                    "Generated Requirements", 
                    st.session_state.generated_requirements, 
                    height=300, 
                    key="generated_requirements_box",
                    disabled=True
                )
        else:
            # Button to generate requirements from the file
           
            if st.button("Generate Requirements"):
                output = generate_requirements(st.session_state.selected_file, llm_url)
                st.session_state.generated_requirements = output
                st.experimental_rerun()  # Force the app to rerun to display updated requirements


# Tab 2: Generated Requirement Files
with tabs[1]:
    st.subheader("📄 Generated Requirements Files")
    
    # List all saved requirements files
    generated_files = ["Select a file..."]+list_generated_files()
    if generated_files:
        selected_file = st.selectbox("Select a file to view/edit:", generated_files, key="select_generated_file")
        if selected_file:
            file_path = os.path.join("requirements", selected_file)
            content = read_file(file_path)
            #Display only the file content and not the error message
            if not content.startswith("Error"):
                edited_content = st.text_area(
                    f"Contents of {selected_file}", 
                    content, 
                    height=300, 
                    key="generated_files_content"
                )
            if st.button("Save Edited File"):
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(edited_content)
                    st.success(f"File '{selected_file}' saved successfully.")
                except Exception as e:
                    st.error(f"Error saving file: {e}")
    else:
        st.write("No generated requirements files found. Generate requirements to see them here.")
# Tab 3: System Requirements Workbench
with tabs[2]:
    st.subheader("📄 Functional Requirements")

    # Load and display groupings
    generated_groupings = ["Select a grouping/tag ...", "<All>"] + load_groupings()
    selected_grouping = st.selectbox("Select a grouping/tag:", generated_groupings, key="select_groupings")

    if selected_grouping and not selected_grouping.startswith("Select a grouping"):
        # Convert selected grouping to uppercase for file matching
        tag_name_upper = selected_grouping.upper()
        system_requirements_folder = os.path.join("requirements", "system_requirements")
        file_path = None

        # Check if a file exists for the selected grouping
        if os.path.exists(system_requirements_folder):
            for file_name in os.listdir(system_requirements_folder):
                if file_name.startswith(tag_name_upper):
                    file_path = os.path.join(system_requirements_folder, file_name)
                    break

        # "Generate System Requirements" button
        if st.button("Generate Functional Requirements"):
            try:
                output_reqs = generate_system_requirements("./requirements", selected_grouping)
                st.session_state.generated_system_requirements = output_reqs  # Store in session state
                st.success(f"Functional requirements for tag '{selected_grouping}' generated successfully!")
                file_path = None  # Clear the file path to prioritize generated content
            except Exception as e:
                st.error(f"Error generating system requirements: {e}")

        # Determine content to display in the text box
        content_to_display = None
        if "generated_system_requirements" in st.session_state and st.session_state.generated_system_requirements:
            # Prioritize displaying generated requirements
            content_to_display = st.session_state.generated_system_requirements
        elif file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content_to_display = file.read()
            except Exception as e:
                st.error(f"Error reading the file: {e}")

        # Display content in the text box if available
        if content_to_display is not None:
            edited_system_reqs = st.text_area(
                f"System requirements for tag '{selected_grouping}'",
                value=content_to_display,
                height=500,
                key="system_requirements_text_area",
            )

            # Save button to save the modified content
            if st.button("Save Requirements File..."):
                # Ensure folder for saving the file exists
                os.makedirs(system_requirements_folder, exist_ok=True)

                # Determine file name and path
                if not file_path:
                    file_path = os.path.join(system_requirements_folder, f"{tag_name_upper}::system-requirements.txt")

                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(edited_system_reqs)
                    st.success(f"System requirements saved successfully to '{file_path}'.")
                except Exception as e:
                    st.error(f"Error saving requirements: {e}")
        else:
            st.info(f"No system requirements file found for the selected tag '{selected_grouping}'.")
# Tab 4: Modernization Workbench
with tabs[3]:
    st.subheader("📄 Modernization Artifacts")

    # Load generated functional/system requirements files
    generated_system_requirements_files = ["Select functional/system requirements..."] + list_generated_system_requirement_files()
    selected_system_requirements_file = st.selectbox("Select a functional/system requirement file:", generated_system_requirements_files, key="select_system_requirements")

    if selected_system_requirements_file and not selected_system_requirements_file.startswith("Select functional/system requirements"):
        # Display the selected file name
        st.session_state.show_controls = False
        st.markdown(f"**Selected File:** {selected_system_requirements_file}")
        
        # Dropdown for additional options
        modernization_options = ["Select an option...", "Generate data model and SQL", "Generate ORM objects", "Generate APIs", "Generate Test Cases", "Generate UI"]
        selected_option = st.selectbox("Select an operation:", modernization_options, key="select_modernization_option")
        # Display a text area based on the selected option
        if selected_option and not selected_option.startswith("Select an option"):
            if selected_option.startswith("Generate data model"):
                st.session_state.gen_content = generate_datamodel_and_sql(os.path.join('./requirements/system_requirements/',selected_system_requirements_file),llm_url)
                st.markdown(f"### {selected_option}")
                st.text_area(f"Output for '{selected_option}':", st.session_state.gen_content, height=400)
                if st.button("Save Generated Artifact..."):
                    # Ensure folder for saving the file exists
                    system_requirements_folder = os.path.join("requirements", "system_requirements")

                    os.makedirs(system_requirements_folder, exist_ok=True)
                    file_path = os.path.join(system_requirements_folder, "Data Model and SQL Script.txt")

                    try:
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(st.session_state.gen_content)
                        st.success(f"System requirements saved successfully to '{file_path}'.")
                    except Exception as e:
                        st.error(f"Error saving requirements: {e}")

            elif selected_option.startswith("Generate ORM objects"):
                #list all the modules (groupings)
                text_datamodel=""
                text_datamodel = st.text_area("Enter data model :",text_datamodel,height=400)
                if st.button("Generate ORM objects..."):
                   st.session_state.gen_content = generate_orm_objects(text_datamodel,llm_url)
                   st.text_area(f"Output for '{selected_option}':", st.session_state.gen_content, height=400) 
                #st.text_area(f"Output for '{selected_option}':", f"You have selected to {selected_option.lower()} for {os.path.join('./requirements/system_requirements/',selected_system_requirements_file)}.", height=400)
                if not st.session_state.gen_content == "":
                    if st.button("Save Generated Artifact..."):
                        # Ensure folder for saving the file exists
                        system_requirements_folder = os.path.join("requirements", "system_requirements")

                        file_path = os.path.join(system_requirements_folder, "ORM Objects.txt")


                        try:
                            with open(file_path, "w", encoding="utf-8") as file:
                                file.write(st.session_state.gen_content)
                            st.success(f"System requirements saved successfully to '{file_path}'.")
                            #st.session_state.gen_content = ""
                            #st.session_state.show_controls = False
                        except Exception as e:
                            st.error(f"Error saving requirements: {e}")
            elif selected_option.startswith("Generate APIs"):
                text_ORM_objects = ""
                text_ORM_objects= st.text_area("Enter ORM objects :",text_ORM_objects,height=400)
                if st.button("Generate APIs..."):
                   st.session_state.gen_content = generate_API(text_ORM_objects,llm_url)
                   st.text_area(f"Output for '{selected_option}':", st.session_state.gen_content, height=400) 
            elif selected_option.startswith("Generate Test Cases"):
                text_test_cases = ""
                text_test_cases = st.text_area("Enter API code :",text_test_cases,height=400)
                if st.button("Generate Test Cases..."):
                   st.session_state.gen_content = generate_test_cases(text_test_cases,llm_url)
                   st.text_area(f"Output for '{selected_option}':", st.session_state.gen_content, height=400)  
            elif selected_option.startswith("Generate UI"):
                text_UI = ""
                text_UI = st.text_area("Enter Requirements :",text_UI,height=400)
                if st.button("Generate UI..."):
                   st.session_state.gen_content = generate_ui(text_UI,llm_url)
                   st.text_area(f"Output for '{selected_option}':", st.session_state.gen_content, height=400)  
                                                            