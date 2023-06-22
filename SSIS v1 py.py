import csv

class Student:
    def __init__(self):
        self.students = []

    def load_from_file(self):
        try:
            with open('students.csv', 'r') as file:
                reader = csv.reader(file)
                self.students = list(reader)
            print("Student data loaded successfully from file.")
        except FileNotFoundError:
            print("No student data file found.")

    def save_to_file(self):
        with open('students.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.students)
        print("Student data saved successfully to file.")

    def add(self):
        student_id = input("Enter Student ID: ")
        name = input("Enter Student Name: ")

        course_menu = Course()
        course_menu.load_from_file()

        if not course_menu.courses:
            print("There is no existing course yet! Please add a course first.")
            choice = input("\n1. Go to Course Menu\n\nEnter Your Choice: ")
            if choice == '1':
                course_menu.menu()
                course_menu.save_to_file()
                course_menu.load_from_file()
            else:
                self.students.append([student_id, name])
                self.save_to_file()
                print("Student added successfully without a course.")
                return

        course_menu.display_list()
        course_code = input("\nEnter Course Code: ")
        if course_code.lower() == '':
            self.students.append([student_id, name])
            self.save_to_file()
            print("Student added successfully.")
            return

        while not self.is_valid_course(course_code, course_menu.courses):
            print("Invalid course code. Please choose a valid course.")
            course_menu.display_list()
            course_code = input("Enter Course Code (or ENTER to skip adding a course): ")
            if course_code.lower() == '':
                self.students.append([student_id, name])
                self.save_to_file()
                print("Student added successfully.")
                return

        course_name = course_menu.get_course_name(course_code)
        self.students.append([student_id, name, course_code, course_name])
        self.save_to_file()
        course_menu.save_to_file()
        print("Student added successfully.")


    def is_valid_course(self, course_code, courses):
        for course in courses:
            if course[0] == course_code:
                return True
        return False

    def delete(self, student_id):
        for student in self.students:
            if student[0] == student_id:
                self.students.remove(student)
                self.save_to_file()
                print("Student deleted successfully.")
                return
        print("Student not found.")


    def edit(self, student_id):
        for student in self.students:
            if student[0] == student_id:
                print("Select field to edit:")
                print("1. Student ID")
                print("2. Name")
                print("3. Course")
                choice = input("Enter Your Choice: ")
                if choice == '1':
                    student[0] = input("Enter New Student ID: ")
                    self.save_to_file()
                    print("Student edited successfully.")
                elif choice == '2':
                    student[1] = input("Enter New Student Name: ")
                    self.save_to_file()
                    print("Student edited successfully.")
                elif choice == '3':
                    course_menu = Course()
                    course_menu.load_from_file()
                    course_menu.display_list()
                    course_code = input("\nEnter new Course Code: ")
                    if course_code.strip().lower() == '0':
                        student.pop(2)
                        student.pop(2)
                        self.save_to_file()
                        print("Course removed successfully.")
                        print("Student edited successfully.")
                    elif course_menu.is_valid_course(course_code):
                        course_name = course_menu.get_course_name(course_code)
                        student[2] = course_code
                        student[3] = course_name
                        self.save_to_file()
                        print("Course updated successfully.")
                        return
                    else:
                        print("\nTHE CODE IS NOT IN THE COURSE LIST. START AGAIN.")
                else:
                    print("Invalid choice.")
                return
        print("Student not found.")

    def display_list(self, courses):
        course_menu = Course()
        course_menu.load_from_file()
        print("\nList of Students:")
        print("{:<10}{:<25}{:<15}{:<15}".format(
            "ID No.", "Name", "Course Code", "Course Name"))
        print("_____________________________________________________________________________")
        for student in self.students:
            course_code = student[2] if len(student) > 2 else None
            course_name = self.get_course_name(course_code, courses) if course_code else "---"
            print("{:<10}{:<25}{:<15}{:<15}".format(
                student[0], student[1], course_code, course_name))

    def search_by_id(self, student_id, courses):
        for student in self.students:
            if student[0] == student_id:
                course_code = student[2] if len(student) > 2 else None
                course_name = self.get_course_name(course_code, courses) if course_code else "---"
                print("\nStudent Found:")
                print("{:<10}{:<25}{:<15}".format(
                    "ID No.", "Name", "Courses Enrolled"))
                print("_____________________________________________________________________________")
                print("{:<10}{:<25}{:<15}".format(
                    student[0], student[1], course_name))
                return
        print("Student not found.")

    def get_course_name(self, course_code, courses):
        for course in courses:
            if course[0] == course_code:
                return course[1]
        return None
    
    def get_course_name(self, course_code, courses):
        for course in courses:
            if course[0] == course_code:
                return course[1]
        return "---" 
    
    def menu(self):
        while True:
            print("\n==== STUDENT MENU ====")
            print("1. Add Student")
            print("2. Delete Student")
            print("3. Edit Student")
            print("4. Display Student List")
            print("5. Search Student by ID")
            print("0. Return to Main Menu")

            choice = input("\nEnter Your Choice: ")
            if choice == '0':
                break
            elif choice == '1':
                self.add()
            elif choice == '2':
                student_id = input("Enter Student ID to Delete: ")
                self.delete(student_id)
            elif choice == '3':
                student_id = input("Enter Student ID to Edit: ")
                self.edit(student_id)
            elif choice == '4':
                course_menu = Course()
                course_menu.load_from_file()
                self.display_list(course_menu.courses)
            elif choice == '5':
                student_id = input("Enter Student ID to Search: ")
                course_menu = Course()
                course_menu.load_from_file()
                self.search_by_id(student_id, course_menu.courses)
            else:
                print("Invalid choice. Please try again.\n")


class Course:
    def __init__(self):
        self.courses = []

    def load_from_file(self):
        try:
            with open('courses.csv', 'r') as file:
                reader = csv.reader(file)
                self.courses = list(reader)
            print("Course data loaded successfully from file.")
        except FileNotFoundError:
            print("\nNo course data file found.")

    def save_to_file(self):
        with open('courses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.courses)
        print("Course data saved successfully to file.")

    def add(self):
        course_code = input("Enter Course Code: ")
        course_title = input("Enter Course Name: ")
        self.courses.append([course_code, course_title])
        self.save_to_file()
        print("Course added successfully.")
    
    def is_valid_course(self, course_code):
        for course in self.courses:
            if course[0] == course_code:
                return True
        return False

    def delete(self, course_code):
        for course in self.courses:
            if course[0] == course_code:
                self.courses.remove(course)
                self.save_to_file()
                print("Course deleted successfully.")
                return
        print("Course not found.")

    def edit(self, course_code):
        for course in self.courses:
            if course[0] == course_code:
                print("What would you like to edit?")
                print("1. Course Code")
                print("2. Course Title")
                edit_choice = input("Enter your choice: ")
                if edit_choice == '1':
                    new_course_code = input("Enter New Course Code: ")
                    course[0] = new_course_code
                elif edit_choice == '2':
                    new_course_title = input("Enter New Course Name: ")
                    course[1] = new_course_title
                else:
                    print("Invalid choice.")
                self.save_to_file()
                print("Course edited successfully.")
                return
        print("Course not found.")


    def display_list(self):
        if self.courses:
            self.load_from_file()
            print("\n=== Course List ===")
            print("{:<15}{:<25}".format("COURSE CODE", "COURSE NAME"))
            print("______________________________________________________________")
            for course in self.courses:
                print("{:<15}{:<25}".format(course[0], course[1]))
        else:
            print("No courses found.")

    def get_course_name(self, course_code):
        for course in self.courses:
            if course[0] == course_code:
                return course[1]
        return None
    
    def menu(self):
        while True:
            print("\n==== COURSE MENU ====")
            print("1. Add Course")
            print("2. Delete Course")
            print("3. Edit Course")
            print("4. Display Course List")
            print("0. Return to Main Menu")

            choice = input("\nEnter Your Choice: ")
            if choice == '0': 
                self.save_to_file()
                break
            elif choice == '1':
                self.add()
            elif choice == '2':
                course_code = input("Enter Course Code to Delete: ")
                self.delete(course_code)
            elif choice == '3':
                course_code = input("Enter Course Code to Edit: ")
                self.edit(course_code)
            elif choice == '4':
                self.load_from_file
                self.display_list()
            else:
                print("Invalid choice. Please try again.\n")


class Main:
    def __init__(self):
        self.student_menu = Student()
        self.course_menu = Course()

    def run(self):
        self.course_menu.load_from_file()
        self.student_menu.load_from_file()

        while True:
            print("\n==== MAIN MENU ====")
            print("1. Student Menu")
            print("2. Course Menu")
            print("0. Exit")

            choice = input("\nEnter Your Choice: ")
            if choice == '0':
                self.student_menu.save_to_file()
                self.course_menu.save_to_file()
                break
            elif choice == '1':
                self.student_menu.menu()
                self.student_menu.save_to_file()
            elif choice == '2':
                self.course_menu.menu()
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == '__main__':
    main_menu = Main()
    main_menu.run()
