import os
from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText  # Importing the ScrolledText widget


# Load the environment variables from .env file
load_dotenv()

# Initialize OpenAI client using the API key from the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def expand_notes():
    brief_notes = text_input.get("1.0", "end-1c")  # Get input from text box
    medical_context = "The following is a medical note in the context of womens health and fertility, napro technology, and synonymous topics:"
    full_prompt = medical_context + brief_notes

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # As of now, OpenAI recommends using "gpt-3.5-turbo" for chat-based applications.
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ]
        )
        print(response) # ADd this line for debugging
        # Access the 'choices' key as per the new response structure
        expanded_text = response.choices[0].message.content  # This is hypothetical code and may need to be adjusted
        text_output.delete("1.0", "end")
        text_output.insert("1.0", expanded_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def clear_input():
    text_input.delete("1.0", "end")  # Clear input text

# Set up the main window
root = tk.Tk()
root.title("Pookie's Assistant")
root.geometry("800x400")

# Create a Text widget for input
text_input = ScrolledText(root, height=10)  # ScrolledText widget for input
text_input.pack()

# Create a Button to trigger notes expansion
expand_button = tk.Button(root, text="Turn into Notes", command=expand_notes)
expand_button.pack()

# Create a Button to clear the input field
clear_button = tk.Button(root, text="Clear Text", command=clear_input)
clear_button.pack()

# Create a ScrolledText widget for showing expanded notes
text_output = ScrolledText(root, height=10, wrap=tk.WORD)  # ScrolledText widget for output
text_output.pack()

root.mainloop()