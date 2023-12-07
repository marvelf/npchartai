Stage 1: Requirement Analysis Assistant - Prompt Generator
Functionality:
The prompt-generator assistant will interact with users (healthcare professionals, compliance experts, etc.) to gather detailed information on what they require from an AI Medical Assistant. This interaction is designed to be iterative, with the assistant asking follow-up questions based on previous answers to delve deeper into the users' needs.

Steps to Develop the Prompt-Generator Assistant:
Define the Objective:

The assistant's primary goal is to extract detailed requirements for an AI Medical Assistant system.
It should understand the context of healthcare documentation and compliance.
Design the Interaction Flow:

Start with broad questions and progress to more detailed inquiries.
Include conditional logic to branch the conversation based on user responses.
Create a Knowledge Base:

Incorporate a database of medical standards, compliance regulations, and common features of medical documentation systems.
The assistant will use this knowledge base to ask informed questions and understand the responses.
Develop Question Templates:

Create templates for different types of requirements such as functional, non-functional, technical, and compliance-related.
These templates will be the basis of the assistant's prompts.
Implement Feedback Loops:

Allow the user to provide feedback on the relevance of the assistant's questions.
Use this feedback to refine the questioning strategy and improve the assistant's effectiveness.
Integrate Contextual Understanding:

The assistant should maintain the context throughout the interaction, allowing for complex requirement gathering.
Implement NLP techniques to parse and understand medical terminology and concepts.
Testing and Iteration:

Conduct tests with actual users to refine the assistant's ability to gather requirements effectively.
Iterate on the prompts based on user feedback and testing results.
Example Prompts from the Prompt-Generator Assistant:
"Can you describe the most time-consuming tasks in your current charting process?"
"Are there specific compliance standards you find challenging to adhere to?"
"What functionalities in your current system do you use most frequently?"
"Can you provide an example of a documentation workflow where you think automation could help?"
"What data security measures are you currently implementing, and how can these be improved?"
Implementation:
To implement this assistant, we will use an AI language model to generate the questions and a user interface to interact with the users. The interface could be a chatbot in a web application or a CLI application, depending on the users' environment.