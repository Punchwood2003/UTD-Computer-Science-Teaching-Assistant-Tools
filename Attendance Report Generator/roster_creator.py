import os
from bs4 import BeautifulSoup

def create_rosters(input_file_name, sections, output_dir_names):
    """
    Given a file containing HTML content, this script extracts the text from the HTML and saves it to a new file.
    Namely, in addition to the student's name, it also separates students into their respective sections.
    The script uses BeautifulSoup to parse the HTML and extract the text. It then writes the extracted text to a new file in a specified format.

    Input:
    - input_file_name: the name of the file containing the HTML content
    - sections: a map between the section ID and the name of the section
    - output_dir_names: a map between the section name and the file to save the output to for that section.
    """
    # Open the input file
    with open(input_file_name, 'r') as input_file:
        # Read the HTML content
        html_content = input_file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the text from the HTML content
    text = soup.get_text()

    # Split the text into lines
    lines = text.split('\n')

    # A map to a list of students in each section
    students_in_sections = {}

    for section_name in sections:
        students_in_sections[section_name] = []

    rows = soup.find_all('tr')
    for row in rows: 
        row_contents = row.contents
        first_name = row_contents[5].get_text()[14:-1]
        last_name = row_contents[7].get_text()[13:-1]
        course_id = row_contents[17].get_text()[19:-2]

        students_in_sections[course_id].append(f"{last_name}, {first_name}")
    
    for section_id in students_in_sections:
        # Get the section name from the sections dictionary
        section_name = sections[section_id]

        # Get the output file name from the output_dir_names dictionary
        output_file_name = output_dir_names[section_name]

        # Open the output file for writing
        with open(output_file_name, 'w') as output_file:
            # Write each student to the file
            for student in students_in_sections[section_id]:
                output_file.write(student + '\n')

# Create a dictionary of section IDs and their corresponding names
sections = {
    '2252-UTDAL-CS-4349-SEC001-23154': 'CS 4349.001 - MW 11_30am',
    '2252-UTDAL-CS-4349-SEC002-23043': 'CS 4349.002 - MW 8_30am'
}

# Create a dictionary of section names and their corresponding output file names
output_dir_names = {
    'CS 4349.001 - MW 11_30am': './rosters/CS 4349.001 - MW 11_30am.txt',
    'CS 4349.002 - MW 8_30am': './rosters/CS 4349.002 - MW 8_30am.txt'
}

# Create the output directories if they don't exist
for dir_name in output_dir_names.values():
    os.makedirs(os.path.dirname(dir_name), exist_ok=True)
    print(f"Created directory {os.path.dirname(dir_name)}")

# Create the rosters
create_rosters('raw_rosters/CS 4349 - S25.html', sections, output_dir_names)