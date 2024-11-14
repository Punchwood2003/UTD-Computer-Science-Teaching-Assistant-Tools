# Import modules from the standard library
import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime

# Function to save attendance report
def save_attendance(section_var: tk.StringVar, date_entry: tk.Entry, attendance_reports: dict[str, list[str]], attendance_listbox: tk.Listbox) -> None:
    """Function to save attendance report"""
    section = section_var.get()
    if not section or section == "Select a section...":  # Check if no section is selected
        messagebox.showwarning("Warning", "Please select a section first.")
        return
    
    date = date_entry.get()
    if date == "":  # Check if no date is entered
        messagebox.showwarning("Warning", "Please enter a date first.")
        return

    # Check if date is in the correct format
    try:
        datetime.datetime.strptime(date, "%m-%d-%Y") 

        # Check if date is valid
        if datetime.datetime.strptime(date, "%m-%d-%Y").date() > datetime.date.today():
            messagebox.showwarning("Warning", "The date you entered is in the future.")
            return
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid date in the format MM-DD-YYYY.")
        return
    
    if messagebox.askyesno("Confirm", f"Are you sure you want to save the attendance report for {section} on {date}?"):
        report_filename = f"reports/{section}/{date}.txt"
        
        if not os.path.exists(f"reports/{section}"):
            os.makedirs(f"reports/{section}")
        
        with open(report_filename, 'w') as file:
            for name in attendance_reports[section]:
                file.write(name + '\n')
        
        # Clear list after saving
        attendance_reports[section] = []
        update_attendance_listbox(section_var, attendance_listbox, attendance_reports)

# Function to update attendance listbox
def update_attendance_listbox(section_var: tk.StringVar, attendance_listbox: tk.Listbox, attendance_reports: dict[str, list[str]]) -> None:
    """Updates the attendance listbox with the names of students in the current section."""
    section = section_var.get()
    attendance_listbox.delete(0, tk.END)
    for name in attendance_reports[section]:
        attendance_listbox.insert(tk.END, name)

# Function to remove selected student from attendance list
def remove_from_attendance(section_var: tk.StringVar, attendance_listbox: tk.Listbox, attendance_reports: dict[str, list[str]]) -> None:
    """Removes the selected student from the attendance list."""
    section = section_var.get()
    selected_name = attendance_listbox.get(tk.ACTIVE)
    if selected_name in attendance_reports[section]:
        attendance_reports[section].remove(selected_name)
        update_attendance_listbox(section_var, attendance_listbox, attendance_reports)

# Add button to submit the attendance
def add_to_attendance(section_var: tk.StringVar, suggestion_listbox: tk.Listbox, attendance_listbox: tk.Listbox, attendance_reports: dict[str, list[str]]) -> None:
    """Adds the selected student to the attendance list."""
    section = section_var.get()
    name = suggestion_listbox.get(tk.ACTIVE)
    if name and name not in attendance_reports[section]:
        attendance_reports[section].append(name)
        update_attendance_listbox(section_var, attendance_listbox, attendance_reports)
    
    attendance_listbox.see(tk.END)

# Function to load attendance reports for a specific section
def load_reports_for_section(section: str) -> list[str]:
    """Loads previously saved attendance reports for a specific section."""
    reports = []
    section_path = f"reports/{section}"
    
    if os.path.exists(section_path):
        for filename in os.listdir(section_path):
            if filename.endswith(".txt"):
                reports.append(filename.replace(".txt", ""))  # Remove file extension for display
    
    return reports

# Function to load attendance from a specific report
def load_attendance_for_report(section_var: tk.StringVar, report_date: str, attendance_listbox: tk.Listbox, attendance_reports: dict[str, list[str]]) -> None:
    """Loads attendance from a saved report file into the listbox."""
    section = section_var.get()
    report_filename = f"reports/{section}/{report_date}.txt"
    
    if os.path.exists(report_filename):
        with open(report_filename, 'r') as file:
            attendance_reports[section] = [line.strip() for line in file.readlines()]
        update_attendance_listbox(section_var, attendance_listbox, attendance_reports)

# Function to toggle between date entry and report selection dropdown
def toggle_report_mode(report_mode_var: tk.StringVar, report_mode_label: tk.Label, date_entry: tk.Entry, section_var: tk.StringVar, report_dropdown: ttk.Combobox, existing_reports: list[str], save_button: tk.Button, generate_frequency_report_button: tk.Button) -> None:
    """Toggles between date entry and report selection dropdown."""
    # Remoev the buttons from the section frame
    save_button.pack_forget()
    generate_frequency_report_button.pack_forget()

    if report_mode_var.get() == "Create New Report":
        report_mode_label.config(text="Enter Date (MM-DD-YYYY)")
        date_entry.pack(pady=4)
        report_dropdown.pack_forget()
    else:
        report_mode_label.config(text="Select Existing Report")
        date_entry.pack_forget()
        update_report_mode_dropdown(report_mode_var, report_dropdown, existing_reports, section_var)
        report_dropdown.pack(pady=3)
    
    save_button.pack(pady=15)
    generate_frequency_report_button.pack(pady=10)

# Function to update the report mode dropdown
def update_report_mode_dropdown(report_mode_var: tk.StringVar, report_dropdown: ttk.Combobox, existing_reports: list[str], section_var: tk.StringVar) -> None:
    """Updates the report mode dropdown based on the current report mode and section."""
    if report_mode_var.get() == 'Modify Existing Report':
        section = section_var.get()
        existing_reports.clear()
        existing_reports.extend(load_reports_for_section(section))  # Load reports for the selected section
        report_dropdown['values'] = existing_reports
        report_dropdown.set("Select a report..." if existing_reports else "No Reports Available")

# Function to load selected report's attendance into the listbox
def on_report_selection(report_dropdown: ttk.Combobox, existing_reports: list[str], section_var: tk.StringVar, attendance_listbox: tk.Listbox, attendance_reports: dict[str, list[str]], date_entry: tk.Entry) -> None:
    """Loads the selected report's attendance into the listbox."""
    selected_report = report_dropdown.get()
    if selected_report and selected_report in existing_reports:
        load_attendance_for_report(section_var, selected_report, attendance_listbox, attendance_reports)

    # Update the date entry with the date of the selected report so that the user can update the file when saving
    date_entry.delete(0, tk.END)
    date_entry.insert(0, selected_report)
