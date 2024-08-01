import os
import openai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText  # Importing the ScrolledText widget


# Load the environment variables from .env file
load_dotenv()

# Initialize OpenAI client using the API key from the environment variable
openai.api_key=os.getenv("OPENAI_API_KEY")

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
    else:
        messagebox.showwarning("Save Conversation", "Save operation cancelled.")


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

# List of markdown file paths
markdown_files = ["Patient 1.md", "Patient 2.md", "Patient 3.md", "Patient 4.md", 
                  "Patient 5.md", "Patient 6.md", "Patient 7.md", "Patient 8.md", 
                  "Patient 9.md", "P1output.md"]

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

# Global list to store chat instances
chat_history = []

def update_chat_history():
    # Update Listbox with the titles of each chat
    chat_list.delete(0, tk.END)  # Clear current list
    for index, chat in enumerate(chat_history):
        chat_list.insert(index, f"Chat {index+1}")  # Add chat to the list

def load_chat(event):
    # Load the selected chat instance
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        input_text.delete("1.0", tk.END)
        output_text.delete("1.0", tk.END)
        input_text.insert("1.0", chat_history[index]['input'])
        output_text.insert("1.0", chat_history[index]['output'])

def save_conversation():
    # After saving the conversation to a file, also save it to chat history
    chat_instance = {'input': input_text.get("1.0", "end-1c"), 'output': output_text.get("1.0", "end-1c")}
    chat_history.append(chat_instance)
    update_chat_history()

def clear_input():
    text_input.delete("1.0", "end")  # Clear input text

# Set up the main window
root = tk.Tk()
root.title("Pookie's Assistant")
root.geometry("800x600")

# Create a Listbox to display chat history
chat_list = tk.Listbox(root)
chat_list.pack(side='left', fill='y')
chat_list.bind('<<ListboxSelect>>', load_chat)

# Create a Text widget for input with scroll bar
text_input = ScrolledText(root, height=10, wrap=tk.WORD)
text_input.pack(fill='x')  # Fill only horizontally

# Define the frame for buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack(fill='x', padx=5, pady=5)  # Add padding

# Create the buttons and pack them into the buttons_frame
expand_button = tk.Button(buttons_frame, text="Turn into Notes", command=expand_notes)
expand_button.pack(side='left', padx=5, pady=5)  # Add some padding

clear_button = tk.Button(buttons_frame, text="Clear Text", command=clear_input)
clear_button.pack(side='left', padx=5, pady=5)  # Add some padding

save_button = tk.Button(buttons_frame, text="Save Conversation", command=save_conversation)
save_button.pack(side='left', padx=5, pady=5)  # Add some padding

# Create a ScrolledText widget for showing expanded notes
text_output = ScrolledText(root, wrap=tk.WORD)
text_output.pack(fill='both', expand=True)  # Fill both directions and allow vertical expansion

root.mainloop()
