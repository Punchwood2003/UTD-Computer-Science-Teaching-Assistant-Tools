import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.TreeMap;

/**
 * The {@link Absences} class is a program that reads a CSV file of absences and
 * prints out a report of the absences.
 * 
 * <p>
 * The CSV file should be in the following format:
 * <code style="display: block; white-space: pre-wrap;">
 * 	DATE_1,NAME_OF_STUDENT_1,NAME_OF_STUDENT_2,…,NAME_OF_STUDENT_N
 * 	DATE_2,NAME_OF_STUDENT_1,NAME_OF_STUDENT_2,…,NAME_OF_STUDENT_N
 * 	⋮
 * 	DATE_N,NAME_OF_STUDENT_1,NAME_OF_STUDENT_2,…,NAME_OF_STUDENT_N
 * </code>
 *
 * The absences report will be formatted as follows:
 * <code style="display: block; white-space: pre-wrap;">
 * 	NAME_OF_STUDENT_1 (NUMBER_OF_ABSENCES): DATE_OF_ABSENCE_1, DATE_OF_ABSENCE_2, …, DATE_OF_ABSENCE_N
 * 	NAME_OF_STUDENT_2 (NUMBER_OF_ABSENCES): DATE_OF_ABSENCE_1, DATE_OF_ABSENCE_2, …, DATE_OF_ABSENCE_N
 * 	⋮
 * 	NAME_OF_STUDENT_M (NUMBER_OF_ABSENCES): DATE_OF_ABSENCE_1, DATE_OF_ABSENCE_2, …, DATE_OF_ABSENCE_N
 * 	
 * 	----------------------------------------------------
 * 	Students who reached 3 or more absences as of DATE_1:
 * 	NAME_OF_STUDENT_1
 * 	NAME_OF_STUDENT_2
 * 	⋮
 * 	NAME_OF_STUDENT_N
 * 	----------------------------------------------------
 * 	Students who reached 3 or more absences as of DATE_2:
 * 	NAME_OF_STUDENT_1
 * 	NAME_OF_STUDENT_2
 * 	⋮
 * 	NAME_OF_STUDENT_N
 * 	----------------------------------------------------
 * 	⋮
 * 	----------------------------------------------------
 * 	Students who reached 3 or more absences as of DATE_N:
 * 	NAME_OF_STUDENT_1
 * 	NAME_OF_STUDENT_2
 * 	⋮
 * 	NAME_OF_STUDENT_N
 * 	----------------------------------------------------
 * </code>
 * 
 * @author MatthewSheldon
 */
public class Absences {
	class Student implements Comparable<Student> {
		public String name;
		public ArrayList<String> absences;

		public Student(String name) {
			this.name = name;
			this.absences = new ArrayList<String>();
		}

		public void addAbsence(String absence) {
			absences.add(absence);
		}

		@Override
		public int compareTo(Student other) {
			int comp = Integer.compare(other.absences.size(), this.absences.size());
			return comp == 0 ? this.name.compareTo(other.name) : comp;
		}

		@Override
		public String toString() {
			return String.format("%s (%d): %s", this.name, this.absences.size(),
					this.absences.toString().replaceAll("[\\[\\]]", ""));
		}
	}

	public static void main(String[] args) throws IOException {
		new Absences().run();
	}

	public void run() throws IOException {
		BufferedReader file = new BufferedReader(new FileReader("absences.csv"));
		PrintWriter out = new PrintWriter(new File("absences_report.txt"));

		HashMap<String, Student> nameToStudent = new HashMap<String, Student>();
		String line = file.readLine();
		while (line != null) {
			String[] arr = line.split("\\s*,\\s*");
			String dateOrAssignment = arr[0];

			for (int i = 1; i < arr.length; i++) {
				Student s = nameToStudent.containsKey(arr[i]) ? nameToStudent.get(arr[i]) : new Student(arr[i]);
				s.addAbsence(dateOrAssignment);
				nameToStudent.put(arr[i], s);
			}

			line = file.readLine();
		}

		file.close();

		ArrayList<Student> students = new ArrayList<Student>();
		nameToStudent.keySet().forEach(name -> students.add(nameToStudent.get(name)));
		Collections.sort(students);

		students.forEach(s -> out.println(s));

		TreeMap<String, ArrayList<Student>> dateThreeAbsences = new TreeMap<String, ArrayList<Student>>();
		students.forEach(s -> {
			if (s.absences.size() >= 3) {
				String date = s.absences.get(2);
				ArrayList<Student> list = dateThreeAbsences.containsKey(date) ? dateThreeAbsences.get(date)
						: new ArrayList<Student>();
				list.add(s);
				dateThreeAbsences.put(date, list);
			}
		});

		out.println();
		dateThreeAbsences.keySet().forEach(date -> {
			out.println("----------------------------------------------------");
			out.printf("Students who reached 3 or more absences as of %s:\n", date);
			dateThreeAbsences.get(date).forEach(student -> out.println(student.name));
		});
		out.println("----------------------------------------------------");

		out.close();
	}
}
