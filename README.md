# UTD-Computer-Science-Teaching-Assistant-Tools

---

## Table of Contents

- [UTD-Computer-Science-Teaching-Assistant-Tools](#utd-computer-science-teaching-assistant-tools)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Projects](#projects)
    - [Local C++ Development Setup](#local-c-development-setup)
    - [Absences Report](#absences-report)
    - [Attendance Report Generator](#attendance-report-generator)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

---

## About

This project is a collection of tools that I developed as a Teaching Assistant / Grader for the University of Texas at Dallas Computer Science Department.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

## Projects
This section will list all of the projects contained in this repository, what they are used for, and why they were created.

### Local C++ Development Setup

This project was created to help freshman Computer Science students (CS 1436) be able to develop C++ programs on their local (windows) computers, despite having limited experience with the language or setting up a development environment. The project includes a step-by-step guide on how to run the provided script to automatically install the necessary tools, libraries, compilers, IDEs, and extensions. The guide was written in LaTeX and the script was written for use in PowerShell.

- [Local C++ Development Setup Script](./Local%20C++%20Development%20Setup%20(Windows)/install_cpp_windows.ps1)
- [Local C++ Development Setup Guide](./Local%20C%2B%2B%20Development%20Setup%20(Windows)/CS%201436.0L1%20%26%20003%20-%20Local%20C%2B%2B%20Development%20Environment%20Setup%20(Windows).pdf)

### Absences Report

This project was created to help in determining the absences of students in a semester, as well as identifying at what point students had three or more absences in a semester. This was created to help determine when to touch base with students in CS 1335 to see if they are still enrolled in the course, or if anything else needs to be addressed. The project is a simple Java program that takes in a list of students and their absences, and outputs a report of the students who have three or more absences and if so, when they reached three or more absences.

- [Absences Report Main Program](./Absences%20Report/src/Absences.java)

### Attendance Report Generator

This project was developed for CS 1436 and is essentially a more robust version of the [Absences Report](#absences-report) project, as it allows the user to create a report of students' attendance for a given day throughuout the semester, obtain a frequency report of attendance, and provides a better GUI for the user to input the students' names and their absences. Since all attendance throughout the semester had been taken on a physical sheet of paper, a large inspiration for this project was to create a program that would more quickly allow the user to enter the names of the students, especially if they were written poorly or misspelled. This is accomplished by using fuzzy string matching to find the closest match to the student's name, and then allowing the user to select the correct name from a list of suggestions. The project is written in Python and uses the tkinter library for the GUI.

- [Attendance Report Generator Main Program](./Attendance%20Report%20Generator/main.py)

---

## License

This project is licensed under the **GNU General Public License v3 (GPL-3.0)**, with the following additional terms:

- **Non-commercial use only**: You may use, modify, and distribute this software for **non-commercial purposes only**. Commercial use, including but not limited to selling, renting, sublicensing, or using the software in any for-profit service, is **not permitted** without express written permission from the original copyright holder.
- **Attribution**: You must give appropriate credit to the original author(s) when redistributing or modifying the software (or any derivative works). You must also include a copy of this license with the software, ensuring that the terms of this license apply to the modified version as well.

If you wish to use this software for commercial purposes, please contact the author, [Matthew Sheldon](mailto:mattsheldon@gmail.com), for a commercial license.

For the full text of the GPL-3.0 license, please see the [LICENSE file](./LICENSE).

---

## Acknowledgments

All of the works included in this project, including but not limited to source code, documentation, scripts, and other materials, were, written, in whole, by Matthew Sheldon. The following is a list of all of the third-party works that were used in this project and were not developed by Matthew Sheldon:

- [Attendance Report Generator](./Attendance%20Report%20Generator/)
  - fuzzywuzzy
    - Author(s): [seatgeek](https://pypi.org/user/seatgeek/)
    - FuzzyWuzzy | [PyPi](https://pypi.org/project/fuzzywuzzy/)
    - FuzzyWuzzy | [GitHub](https://github.com/seatgeek/fuzzywuzzy)
  - python-levenshtein 
    - Author(s): [dorinaj](https://pypi.org/user/dorianj/), [Lukelmhoff](https://pypi.org/user/LukeImhoff/), [maxbachmann](https://pypi.org/user/maxbachmann/), [miohtama](https://pypi.org/user/miohtama/), and [ztane](https://pypi.org/user/ztane/) 
    - Levenshtein | [PyPi](https://pypi.org/project/python-Levenshtein/)
    - Levenshtein | [GitHub](https://github.com/rapidfuzz/python-Levenshtein)