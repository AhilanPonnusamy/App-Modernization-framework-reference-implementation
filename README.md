# Application Modernization Framework - Reference Implementation

This comprehensive guide provides step-by-step instructions for configuring and running the App modernization reference implementation tool. This tool is developed by a LLM using progressive prompting technique with minimal edits. It can be deployed and run on local machine and can be modified to work with your model of choice with minimal code changes.
The following is the sysem specification that I used for this project, A lower configuration will work just fine apart from notable response time delay.

**System Specifications:**

- Device: MacBook Pro
- Chip: Apple M2 Pro
- RAM: 32 GB 

## Prerequisites

1.  Install Python,pip, and Streamlit if it is not already installed. You need Python version 3.8 or higher.

2. Download this code repository (install git if it is not already setup, You can also downlod the zip file directly from the main page under code option as an alternate)

3. Download and serve the grantile code model in InstructLab as shown below. 
```
  $ ilab model serve --model-path models/granite-8b-code-instruct-128k.Q5_K_M.gguf
```
4. Download the Spring-petclinic application from **https://github.com/spring-projects/spring-petclinic/tree/main?tab=readme-ov-file**.
5. In a new terminal start the App modernization assistant tool.
```
  $ streamlit run requirements_manager_ui.py
```
>[!WARNING]
>This tool is a reference implementation of the proposed app modernization framework. Necessary updates must be made to extend this for entperise use.
> 
## Generating Requirements for Legacy Application

1. Enter the folder path for the Spring petclinic application and Load the project structure e.g. spring-petclinic/src/main/resources/templates (User Interface layer)
![App UI](./images/LoadfProject_main.png)

2. Select **createOrUpdateOwnerForm.html** under owners folder and click on **Generate Requirements** button under the **File Workbench** tab. The system will display the generated requirements in a text box, make necessary changes and save the requirments by adding a new module name called "owners" from the "Select a module name/tag" drop down.
![App UI](./images/SaveRequirments_main.png)    

3. Repeat the process and save generated requirements for all files under owners, pets and vets folders. Make sure to enter/select the appropriate module name before saving the requiements. e.g. All requirement files under vets should be saved with **vets** as the module name etc. **This step is important to group all related requirments together which will be used in the following steps.**

>[!NOTE]
>You may use the **Generated Requirement Files** tab functionality to edit the requirement files at any time once the requirements are created.
 
4. Navigate to the **Functional Requirements Workbench** tab. Select "\<All\>" as the grouping name and click on **Generate Functional Requirements** button to generate consolidated requirements for owners, pets and vets interaction layer. Review and make necessary edits and save the requirements file.
![App UI](./images/Generate_Consolidate_Requirements.png)

>[!NOTE]
>Depending on your project, you may also want to generate functional requirements for other layers such as business logic tier, partner APIs and batch scripts.

## Generating Artifacts for the new Application

### This reference implementation uses Quarkus framework,React and postgres as the target platform.

5. Navigate to the **Moderization Workbench** tab. Select the newly created requirements file **\<ALL\>::system-requirements.txt** from the drop down and select **Generate data model and SQL** option from the second drop down. The system will invoke the LLM and display the generated output. Review the output for completeness, make necessary edits and save it.
![App UI](./images/DatamodelandSQL.png)

6. Copy owners table sql script. Select **Generate ORM objects** from the second drop down and click on **Generate ORM objects**  button. Wait for the LLM response, review the output for accuracy and completeness and save the artifact.
![App UI](./images/GenerateORM.png)

7. Repeat the above step for generating API code by selecting **Generate APIs** as the operation in the second drop down, providing ORM object as the input and clicking on **Generate APIs** button.
![App UI](./images/GenerateAPIs.png)   

8. Repeat the above step for generating Test cases for the APIs by selecting **Generate Test Cases** as the operation in the second drop down and clicking on **Generate Test Cases** button.
![App UI](./images/GenerateTestcases.png)

9. The next step is to generate UI code, for this, select **Generate UI** as the operation from the second drop down, copy and paste the functional requirements of the desired screen (e.g.,**OWNERS::owners-ownerDetails.html-requirements.txt**)  in the **Enter Requirements** text box and click on **Generate UI** button.
![App UI](./images/GenerateUI.png)

> [!NOTE]
> The reference implementation utilizes generic prompts to facilitate seamless transitions between different models. However, employing model specific prompt templates, such as those provided here(https://www.ibm.com/granite/docs/models/code/#code-generation), can significantly enhance the accuracy and consistency of the responses.
>
>This exercise focuses only on generating functional requirements.However, the same processs can be applied to generate non-functional requirements from load test scripts e.g. JMeter and other articats.
