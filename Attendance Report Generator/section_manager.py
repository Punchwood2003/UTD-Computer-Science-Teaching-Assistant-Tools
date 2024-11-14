# Import modules from the standard library
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import os

# Import functions from local modules
from attendance_report_file_manager import update_report_mode_dropdown
from name_suggestion import on_name_entry

# Function to dynamically load sections and students
def load_sections(ROSTER_DIR: str, sections: dict) -> None:
    """Loads sections and their corresponding students from the /rosters directory."""
    sections.clear()

    # Check if the rosters directory exists
    if not os.path.exists(ROSTER_DIR):
        os.makedirs(ROSTER_DIR)

    # Loop through all text files in the /rosters directory
    for filename in os.listdir(ROSTER_DIR):
        if filename.endswith('.txt'):
            section_name = os.path.splitext(filename)[0]  # Extract section name from filename
            student_list = load_students_from_file(os.path.join(ROSTER_DIR, filename))
            sections[section_name] = student_list

# Function to read student names from a roster file
def load_students_from_file(filename: str) -> list[str]:
    """Reads student names from a file and returns them as a list."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]
    
# Function to add a new roster
def add_new_roster(students: dict, ROSTER_DIR: str, section_dropdown: ttk.Combobox, section_var: tk.StringVar) -> None:
    """Adds a new roster to the /rosters directory."""
    # Open a file dialog to select a file containing student names
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    
    if file_path:
        # Read the student names from the selected file
        student_names = []
        with open(file_path, 'r') as file:
            student_names = file.readlines()
        
        # Strip newlines and whitespace from each student name
        student_list = [name.strip() for name in student_names]
        
        # Ask for a section name for the new roster
        section_name = simpledialog.askstring("New Section", "Enter the name of the new section:")
        if section_name:
            # Save the student names to a new roster file
            roster_file_path = os.path.join(ROSTER_DIR, f"{section_name}.txt")
            with open(roster_file_path, 'w') as file:
                for name in student_list:
                    file.write(name + '\n')
                file.flush()
                file.close()
            
            # Reload sections and update the dropdown
            load_sections(ROSTER_DIR, students)  # Reload students after adding a new roster
            section_dropdown['values'] = list(students.keys())
            section_var.set(section_name)  # Set the new section as the current one

# Function to remove an existing roster
def remove_roster(students: dict, section_var: tk.StringVar, ROSTER_DIR: str, section_dropdown: ttk.Combobox) -> None:
    """Removes an existing roster from the /rosters directory."""
    section_to_remove = section_var.get()
    if section_to_remove in students:
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the roster for {section_to_remove}?")
        if confirm:
            # Remove the file
            file_path = os.path.join(ROSTER_DIR, f"{section_to_remove}.txt")
            os.remove(file_path)

            # Reload sections and update the dropdown
            load_sections(ROSTER_DIR, students)  # Reload students after removing a roster
            section_dropdown['values'] = list(students.keys())
            if students:
                section_var.set(list(students.keys())[0])  # Set to the first section if available
            else:
                section_var.set("No Sections")  # If no sections left
    else:
        messagebox.showwarning("Warning", "Section not found.")

# Function to update the other sections when a new section is selected
def on_section_selection(report_mode_var: tk.StringVar, report_dropdown: ttk.Combobox, existing_reports: list[str], section_var: tk.StringVar, name_entry: tk.Entry, suggestion_listbox: tk.Listbox, students: dict) -> None:
    """Updates the other sections when a new section is selected."""
    # First, call update_report_mode_dropdown to update the list of known reports
    update_report_mode_dropdown(report_mode_var, report_dropdown, existing_reports, section_var)
    # Then, update the list of students in the attendance listbox
    on_name_entry(name_entry, section_var, students, suggestion_listbox)