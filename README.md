# Application Modernization Framework Reference Implementation

This comprehensive guide provides step-by-step instructions for configuring and running the App modernization reference implementation tool. This tool was developed by LLM using progressive prompting technique with minimal edits. It can be deployed and run on local machine and can be modified to work with your model of choice with minimal code changes.
The following is the sysem specification that I used for this project, I do believe a lower configuration will work just fine.

**System Specifications:**

- Device: MacBook Pro
- Chip: Apple M2 Pro
- RAM: 32 GB 

## Prerequisites

1.  Install Python and pip if it is not already installed. You need Python version 3.8 or higher.

2. Download this code repository (install git if it is not already setup, You can also downlod the zip file directly from the main page under code option as an alternate)

3. Download and serve the grantile codel model in InstructLab as shown below. Make sure the context length (max_ctx_size) is set to a higher number e.g. 100k in the config.yaml file.
```
  $ ilab model serve --model-path models/granite-8b-code-instruct-128k.Q5_K_M.gguf
```
4. Download the Spring-petclinic application from **https://github.com/spring-projects/spring-petclinic/tree/main?tab=readme-ov-file**
5. In a new terminal start the application
```
  $ streamlit run requirements_manager_ui.py
```
>[!WARNING]
>This tool is a reference implementation of the proposed app modernization framework. Necessary updates must be made to extend this for entperise use.
> 
## Generating Requirements for Legacy Application

1. Enter the folder path for the Spring petclinic application and Load the project structure e.g. spring-petclinic/src/main/resources/templates (User Interface layer)
![App UI](./images/LoadProject.png)

3. With **Use RAG** option selected, submit the same question **can you transfer $50 to joseph?** you will now see a more context aware message as shown below
![App UI](./images/WithRAG.jpg)    

>[!WARNING]
>You may periodically face the following context window size error. Clik on the clear conversation button on the left side to flush the data and try again.
 
3. you can try the following prompts to try with **Use RAG** option selected
     - can you transfer $50 to ram?
     - can you transfer $580 to john?
     - can you transfer $100 to peter?
     - can you add joseph to my account?
     - can you add allan to my account?
     - can you remove john from my account?
     - can you remove mark from my account?
   
***Have fun!!!!!***
