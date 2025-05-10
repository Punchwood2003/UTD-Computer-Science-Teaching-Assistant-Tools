# Import modules from the standard library
import tkinter as tk

# Import modules that are in requirements.txt
from fuzzywuzzy import process

# Function to handle name entry
def on_name_entry(name_entry: tk.Entry, section_var: tk.StringVar, students: dict, suggestion_listbox: tk.Listbox) -> None:
    """Handles user input in the name entry field."""
    # Ignore if no selection has been made
    if section_var.get() == "" or section_var.get() == "Select a section...":
        return
    
    query = name_entry.get()
    section = section_var.get()     
    suggestions = suggest_names(query, section, students)
    
    # Update suggestion listbox
    suggestion_listbox.delete(0, tk.END)
    for suggestion in suggestions:
        suggestion_listbox.insert(tk.END, suggestion)

# Function to suggest names
def suggest_names(query: str, section: str, students: dict) -> list:
    """Provides a list of suggested names that are similar to the passed query from the section"""
    student_list = students[section]
    return [name for name, score in process.extract(query, student_list, limit=len(student_list))]
