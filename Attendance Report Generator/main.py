# Import modules from the standard library
import tkinter as tk
from tkinter import ttk 

# Import functions from local modules
from attendance_report_file_manager import save_attendance, remove_from_attendance, add_to_attendance, toggle_report_mode, on_report_selection
from name_suggestion import on_name_entry
from section_manager import load_sections, add_new_roster, remove_roster, on_section_selection
from attendance_frequency import generate_frequency_report


# Global font size variables
header_font_size = 18  # Font size for headers (labels, buttons, etc.)
body_font_size_large = 16  # Larger of two body font sizes
body_font_size_small = 12  # Smaller of two body font sizes

# Directory containing roster files
ROSTER_DIR = './rosters'

# Load the sections when the program starts
students = {}
load_sections(ROSTER_DIR, students)

# Attendance records
attendance_reports = {section: [] for section in students}


#############################
# Create the general layout #
#############################

# Create main window with larger size
root = tk.Tk()
root.title("Attendance Marking")
root.geometry("1280x570")

# Create a PanedWindow to split the layout into 3 vertical sections
paned_window = tk.PanedWindow(root, orient="horizontal", sashwidth=0, sashrelief="flat")
paned_window.pack(fill=tk.BOTH, expand=False)

# SECTION 1: Where the user loads, adds, or removes a roster, as well create a report for a given day
section_frame = tk.Frame(paned_window, padx=10, pady=10)
section_frame.pack(fill=tk.Y, side=tk.LEFT, expand=False)

# SECTION 2: Used for listing suggested names, and allows the user to add a user to the attendance list for a day
attendance_frame = tk.Frame(paned_window, padx=10, pady=10)
attendance_frame.pack(fill=tk.Y, side=tk.LEFT, expand=False)

# SECTION 3: Used for listing those pepole who are in the attendance list for a day, and allows the user to remove a user from the attendance list
list_frame = tk.Frame(paned_window, padx=10, pady=10)
list_frame.pack(fill=tk.Y, side=tk.LEFT, expand=False)

##############################################################
# Create the listboxes and variables shared between sections #
##############################################################

# Used for the list of suggested names
suggestion_listbox = tk.Listbox(attendance_frame, font=("Arial", body_font_size_large), height=12, width=35)

# Used for the list of people in the attendance list
attendance_listbox = tk.Listbox(list_frame, font=("Arial", body_font_size_large), height=16, width=35)

# Variables for report mode and date/report selection
report_mode_var = tk.StringVar(value="Create New Report")  # Default to "Create New Report"
existing_reports = []

###############################################
# SECTION 1: Section selection and date entry #
###############################################

# Section selection
section_var = tk.StringVar(value="")
section_label = tk.Label(section_frame, text="Select Section", font=("Arial", header_font_size))
section_label.pack(pady=10)


# Dynamically load section names into the dropdown menu
section_dropdown = ttk.Combobox(section_frame, textvariable=section_var, values=list(students.keys()), font=("Arial", body_font_size_large))
section_dropdown.set("Select a section..." if students else "No Sections")
section_dropdown.bind("<<ComboboxSelected>>", lambda event: on_section_selection(report_mode_var, report_dropdown, existing_reports, section_var, name_entry, suggestion_listbox, students))
section_dropdown.pack(pady=10)


# Buttons to add and remove rosters
add_roster_button = tk.Button(section_frame, text="Add New Section's Roster", command=lambda: add_new_roster(students, ROSTER_DIR, section_dropdown, section_var), font=("Arial", body_font_size_small))
add_roster_button.pack(pady=10)

remove_roster_button = tk.Button(section_frame, text="Remove Selected Section's Roster", command=lambda: remove_roster(students, section_var, ROSTER_DIR, section_dropdown), font=("Arial", body_font_size_small))
remove_roster_button.pack(pady=0)


# Add some vertical space between the sections
tk.Frame(section_frame).pack(fill=tk.X, pady=10)


# Make a title for this subsection
report_mode_label = tk.Label(section_frame, text="Select Report Mode", font=("Arial", header_font_size))
report_mode_label.pack(pady=0)


# Add a frame to center the radio buttons
report_mode_frame = tk.Frame(section_frame)
report_mode_frame.pack(pady=5)


# Denotes the label that should be placed above the date entry or the existing report dropdown
report_mode_label = tk.Label(section_frame, text="Enter Date (MM-DD-YYYY)", font=("Arial", header_font_size))
report_mode_label.pack(pady=15)


# Add radio buttons for report selection mode
create_report_radio = tk.Radiobutton(report_mode_frame, text="Create New Report", variable=report_mode_var, value="Create New Report", font=("Arial", body_font_size_small), command=lambda: toggle_report_mode(report_mode_var, report_mode_label, date_entry, section_var, report_dropdown, existing_reports, save_button, generate_frequency_report_button))
create_report_radio.pack(anchor="w")

modify_report_radio = tk.Radiobutton(report_mode_frame, text="Modify Existing Report", variable=report_mode_var, value="Modify Existing Report", font=("Arial", body_font_size_small), command=lambda: toggle_report_mode(report_mode_var, report_mode_label, date_entry, section_var, report_dropdown, existing_reports, save_button, generate_frequency_report_button))
modify_report_radio.pack(anchor="w")

report_mode_frame.pack(anchor="center")


# Add a frame to center the date entry and dropdown
date_entry = tk.Entry(section_frame, font=("Arial", body_font_size_large), width=20)  # Increased input field width
date_entry.pack(pady=4)


# Create a dropdown for selecting existing reports, initially hidden
report_dropdown = ttk.Combobox(section_frame, font=("Arial", body_font_size_large), state="readonly", width=30)
report_dropdown.bind("<<ComboboxSelected>>", lambda event: on_report_selection(report_dropdown, existing_reports, section_var, attendance_listbox, attendance_reports, date_entry))


# Save report button 
save_button = tk.Button(section_frame, text="Save Attendance Report", command=lambda: save_attendance(section_var, date_entry, attendance_reports, attendance_listbox), font=("Arial", body_font_size_large))
save_button.pack(pady=15)


# Generate frequency report button
generate_frequency_report_button = tk.Button(section_frame, text="Generate Frequency Report", command=lambda: generate_frequency_report(section_var), font=("Arial", body_font_size_large))
generate_frequency_report_button.pack(pady=10)

######################################################
# SECTION 2: Name entry, suggestions, and add button #
######################################################

# Name entry with suggestions
name_label = tk.Label(attendance_frame, text="Enter Student's Name", font=("Arial", header_font_size))
name_label.pack(pady=10)

name_entry = tk.Entry(attendance_frame, font=("Arial", body_font_size_large), width=30)
name_entry.bind("<KeyRelease>", lambda event: on_name_entry(name_entry, section_var, students, suggestion_listbox))
name_entry.pack(pady=10)

name_label = tk.Label(attendance_frame, text="Suggested Names", font=("Arial", header_font_size))
name_label.pack(pady=10)

# Listbox for the suggested names
suggestion_listbox.pack(pady=10)

# Button used for adding a user to the day's attendance
add_button = tk.Button(attendance_frame, text="Add to Attendance", command=lambda: add_to_attendance(section_var, suggestion_listbox, attendance_listbox, attendance_reports), font=("Arial", body_font_size_large))
add_button.pack(pady=10)

#############################################
# SECTION 3: Attendance list, remove button #
#############################################

# Listbox for the attendance list
name_label = tk.Label(list_frame, text="In Attendance", font=("Arial", header_font_size))
name_label.pack(pady=10)
attendance_listbox.pack(pady=10)

# Remove button to delete selected student from attendance list
remove_button = tk.Button(list_frame, text="Remove Selected", command=lambda: remove_from_attendance(section_var, attendance_listbox, attendance_reports), font=("Arial", body_font_size_large))
remove_button.pack(pady=10)

##############################################
# Add the three sections to the paned window #
##############################################

paned_window.add(section_frame, minsize=340)
paned_window.add(attendance_frame, minsize=420)
paned_window.add(list_frame, minsize=420)

# Run the main loop
root.mainloop()