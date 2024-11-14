# Import modules from the standard library
import tkinter as tk
from tkinter import messagebox
import os

# Given a section, generate a frequency report (CSV file) for the section 
def generate_frequency_report(section_var: tk.StringVar) -> None:
    """
    Generates a frequency report for the given section.
    The two columns in the report are the name of the student and the number of times they attended.
    The names shuolld appear in the same order as in the original roster.
    """
    section = section_var.get()
    # Read all of the attendance reports for the section
    attendance_reports = read_attendance_reports(section)

    # Check if there are any attendance reports for the section
    if attendance_reports != {}:
        if messagebox.askyesno("Confirm", f"Are you sure you want to generate a frequency report for the section {section}?"):
            # Open a file to write the report to
            with open(f"reports/{section}/frequency_report.csv", "w") as file:
                # Write the header row
                file.write("Last Name,First Name,Frequency\n")

                frequency = {}
                
                # Iterate over the attendance reports for the section
                for date in attendance_reports:
                    # Get the list of students who attended the report
                    attendees = attendance_reports[date]
                    
                    # Write the report for each student
                    for attendee in attendees:
                        # Increment the frequency count for the attendee
                        if attendee in frequency:
                            frequency[attendee] += 1
                        else:
                            frequency[attendee] = 1

                # Write the frequency report for each student in the same order as in the original roster
                with open(f"rosters/{section}.txt", "r") as roster_file:
                    for line in roster_file:
                        name = line.strip()
                        if name in frequency:
                            f = frequency[name]
                            # Name is in form of "Last Name, First Name"
                            name = name.split(", ")
                            # Write the frequency report
                            file.write(f"{name[0]},{name[1]},{f}\n")
                        else:
                            # Name simply does not have any attendance
                            name = name.split(", ")
                            # Write the frequency report
                            file.write(f"{name[0]},{name[1]},0\n")
                
                # Flush the file to ensure all data is written
                file.flush()
                # Close the file
                file.close()
                # Alert the user that the report was generated
                messagebox.showinfo("Success", "Frequency report generated successfully.")
    else:
        # Make sure the user has not already selected a section and there just are no attendance reports for the section
        if section_var.get() == "Select a section...":
            # Alert the user that they need to select a section first
            messagebox.showwarning("Warning", "Please select a section first.")
        else:
            messagebox.showwarning("Warning", "There are no attendance reports for the selected section.")

def read_attendance_reports(section: str) -> dict[str, list[str]]:
    """Reads all of the attendance reports for a given section and returns them as a dictionary."""
    attendance_reports = {}
    
    # Check if the reports directory exists
    if os.path.exists(f"reports/{section}"):
        # Loop through all text files in the reports directory
        for filename in os.listdir(f"reports/{section}"):
            if filename.endswith(".txt"):
                report_name = os.path.splitext(filename)[0]  # Extract report name/date from filename
                # Load the attendance report
                student_list = []
                with open(f"reports/{section}/{filename}", "r") as report_file:
                    for line in report_file:
                        student_list.append(line.strip())
                
                attendance_reports[report_name] = student_list
        
        return attendance_reports
    else:
        return {}