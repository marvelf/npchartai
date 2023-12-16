import os
import openai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox, filedialog, Scrollbar, Listbox
from tkinter.scrolledtext import ScrolledText
import json 

# Define the filename where chat history will be saved
CHAT_HISTORY_FILE = 'chat_history.json'

def load_chat_history():
    # Load chat history from a file
    try:
        with open(CHAT_HISTORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file does not exist, return an empty list
        return []
    except json.JSONDecodeError:
        # Handle the exception if the file content is not valid JSON
        print("Error reading the chat history file. Starting with an empty chat history.")
        return []

def save_chat_history():
    # Save chat history to a file
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(chat_history, file, indent=4)

# Load the environment variables from .env file
load_dotenv()

# Initialize OpenAI client using the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global list to store chat instances
chat_history = load_chat_history()

def update_chat_history():
    # Update Listbox with the titles of each chat
    chat_list.delete(0, tk.END)  # Clear current list
    for index, chat in enumerate(chat_history):
        chat_list.insert(index, f"Chat {index + 1}")

def load_chat(event):
    # Load the selected chat instance
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        text_input.delete("1.0", tk.END)
        text_output.delete("1.0", tk.END)
        text_input.insert("1.0", chat_history[index]['input'])
        text_output.insert("1.0", chat_history[index]['output'])

def save_conversation():
    # Get the text from input and output widgets
    input_text = text_input.get("1.0", "end-1c")
    output_text = text_output.get("1.0", "end-1c")
    
    # Ask the user for a file location to save the conversation
    filename = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Text files", "*.md"), ("All files", "*.*")],
        title="Save conversation as..."
    )
    
    # Check if a filename was given
    if filename:
        # Write the conversation to the file
        with open(filename, "w") as file:
            file.write("Input:\n" + input_text + "\n\n")
            file.write("Response:\n" + output_text + "\n")
        messagebox.showinfo("Save Conversation", "The conversation has been saved.")
        
        # Append the chat to the history and save it to the JSON file
        chat_instance = {'input': input_text, 'output': output_text}
        chat_history.append(chat_instance)
        save_chat_history()  # This will save the entire chat history to a file
        update_chat_history()
    else:
        messagebox.showwarning("Save Conversation", "Save operation cancelled.")

# List of markdown file paths
markdown_files = ["Patient 1.md", "Patient 2.md", "Patient 3.md", "Patient 4.md", 
                  "Patient 5.md", "Patient 6.md", "Patient 7.md", "Patient 8.md", 
                  "Patient 9.md", "P1output.md", "P6output.md", "P6response2test.md", "P8output.md", "P9output.md"]

# Set up the main window
root = tk.Tk()
root.title("Pookie's Assistant")
root.geometry("900x600")
 # Set the root window background color

# Define the layout using PanedWindow for better resizing behavior
main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
main_pane.pack(fill=tk.BOTH, expand=1)

# Create a Listbox to display chat history and pack into a frame for scrolling
chat_frame = tk.Frame(main_pane)  # Add it to main_pane instead of root
scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_list = Listbox(chat_frame, yscrollcommand=scrollbar.set)
chat_list.pack(expand=True, fill=tk.BOTH)
scrollbar.config(command=chat_list.yview)
chat_list.bind('<<ListboxSelect>>', load_chat)

def read_acronyms_md():
    acronyms_context = ""
    try:
        with open('acronyms.md', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if '- **' in line:  # Detects acronym lines
                    acronym, explanation = line.split('**: ')
                    acronyms_context += acronym.strip('- **') + " stands for " + explanation
    except FileNotFoundError:
        print("Acronyms file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return acronyms_context

# Add chat_frame to the main_pane
main_pane.add(chat_frame)

# Create a Frame for text input/output and buttons, add it to the main pane
text_and_buttons_frame = tk.Frame(main_pane)
main_pane.add(text_and_buttons_frame)

# Create a Text widget for input with scroll bar
text_input = ScrolledText(text_and_buttons_frame, height=13, wrap=tk.WORD)
# Allow expansion
text_input.pack(fill=tk.BOTH, expand=1, pady=5)


# Aggregate context from all files
def aggregate_context_from_files(file_list):
    aggregated_context = ""
    for file_name in file_list:
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    # Add logic here to process each line
                    # For example, you might want to include only key sentences or phrases
                    aggregated_context += line.strip() + " "
        except FileNotFoundError:
            print(f"{file_name} not found.")
        except Exception as e:
            print(f"An error occurred while reading {file_name}: {e}")

    # You might need to truncate or process the aggregated_context to fit the token limit
    return aggregated_context

def expand_notes():
    brief_notes = text_input.get("1.0", "end-1c")  # Get input from text box
    acronyms_context = read_acronyms_md()  # Get the context from acronyms.md
    file_context = aggregate_context_from_files(markdown_files)  # Get aggregated context from files
    medical_context = "Expand the following brief notes into a full medical chart entry based solely on the information provided:"
    full_prompt = medical_context + acronyms_context + file_context + brief_notes

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # As of now, OpenAI recommends using "gpt-3.5-turbo" for chat-based applications.
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ]
        )
        print(response) # Add this line for debugging
        # Access the 'choices' key as per the new response structure
        expanded_text = response.choices[0].message.content  # This is hypothetical code and may need to be adjusted
        text_output.delete("1.0", "end")
        text_output.insert("1.0", expanded_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    

def save_chat_instance(input_text, output_text):
    chat_instance = {'input': input_text, 'output': output_text}
    chat_history.append(chat_instance)
    update_chat_history()

def clear_input():
    text_input.delete("1.0", "end")  # Clear input text
    text_output.delect("1.0", "end")  # Clear output text


# Define the frame for buttons and add it below the input text
buttons_frame = tk.Frame(text_and_buttons_frame)
buttons_frame.pack(fill=tk.Y, padx=5, pady=5)  # Fill only horizontally

# Create buttons and pack them into the buttons_frame
expand_button = tk.Button(buttons_frame, text="Turn into Notes", command=expand_notes, bg="lightblue")
expand_button.pack(side=tk.TOP, padx=5, pady=5)

clear_button = tk.Button(buttons_frame, text="Clear Text", command=clear_input)
clear_button.pack(side=tk.TOP, padx=5, pady=5)

save_button = tk.Button(buttons_frame, text="Save Conversation", command=save_conversation, bg="lightblue")
save_button.pack(side=tk.TOP, padx=5, pady=5)

# Create a ScrolledText widget for showing expanded notes, add it below buttons
text_output = ScrolledText(text_and_buttons_frame, wrap=tk.WORD)
text_output.pack(fill=tk.BOTH, expand=1, pady=20)  # Allow expansion

root.mainloop()