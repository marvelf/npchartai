import os
import openai
import time  # Import the time module
from dotenv import load_dotenv


# Load the environment variables from .env file
load_dotenv()

# Initialize OpenAI client using the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create the MedAI assistant
assistant = openai.beta.assistants.create(
    name='MedAI',
    instructions='You are an AI assistant specialized in medical transcription. Expand brief medical notes into comprehensive chart notes, adhering to the user\'s style of documentation.',
    model='gpt-3.5-turbo'
)

print('MedAI assistant created....')

# Function to save the assistant ID
def save_assistant_id(assistant_id, filename="medai_assistant_id.txt"):
    with open(filename, 'w') as file:
        file.write(assistant_id)

# Save the MedAI assistant ID
save_assistant_id(assistant.id)

# Create a thread for MedAI interactions
thread = openai.beta.threads.create()
print(f'Thread created for MedAI...{thread.id}')

# Function to save the thread ID
def save_thread_id(thread_id, filename="medai_thread_id.txt"):
    with open(filename, 'w') as file:
        file.write(thread_id)

# Save the thread ID
save_thread_id(thread.id)

# Function to process user input and run MedAI
def run_medai(thread_id, assistant_id, user_input):
    # Add message to thread
    message = openai.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=user_input
    )

    # Run the MedAI assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Wait for the run to complete
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status in ['completed', 'failed', 'cancelled']:
            print(f'Run completed with status: {run_status.status}')
            break
        else:
            print('MedAI run still in progress, waiting...')
            time.sleep(5)

    # Fetch and print the messages after the run is completed
    print('Run finished, fetching messages...')
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    for message in messages.data:
        print(f'{message.role.title()}: {message.content[0].text.value}')

        # Example of using MedAI
user_input = "1. Abnormal androgen: Decreased testosterone / DHEA DHEA - 25mg, also discussed 2. Normal TSH, low T3 ashwagandha, medcaps T3, and T-150. Discussed RBA 3. ethylation homocysteine - send to quest 4. Hx of Neuroblastoma 5. Pt has possible of kidney cancer...concerned with testosterone and kidney cancer???"
run_medai(thread.id, assistant.id, user_input)