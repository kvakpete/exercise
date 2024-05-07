def create_student(students):
    while True:
        first_name = input("Enter student's first name: ")
        last_name = input("Enter student's last name: ")
        class_name = input("Enter student's class name: ")
        students[(first_name, last_name)] = class_name
        print("Student created successfully.")
        break

def create_teacher(teachers):
    while True:
        first_name = input("Enter teacher's first name: ")
        last_name = input("Enter teacher's last name: ")
        subject = input("Enter teacher's subject: ")
        classes_taught = []
        while True:
            class_name = input("Enter class name taught by the teacher (leave empty to stop): ")
            if not class_name:
                break
            classes_taught.append(class_name)
        teachers[(first_name, last_name)] = {'subject': subject, 'classes_taught': classes_taught}
        print("Teacher created successfully.")
        break

def create_homeroom_teacher(homeroom_teachers):
    while True:
        first_name = input("Enter homeroom teacher's first name: ")
        last_name = input("Enter homeroom teacher's last name: ")
        class_name = input("Enter homeroom teacher's class name: ")
        homeroom_teachers[(first_name, last_name)] = class_name
        print("Homeroom teacher created successfully.")
        break

def manage_class(students, homeroom_teachers):
    class_name = input("Enter class name to display: ")
    print(f"\nStudents in class {class_name}:")
    for student, cls in students.items():
        if cls == class_name:
            print(f"{student[0]} {student[1]}")
    print(f"Homeroom teacher for class {class_name}:")
    for teacher, cls in homeroom_teachers.items():
        if cls == class_name:
            print(f"{teacher[0]} {teacher[1]}")

def manage_student(students, teachers):
    first_name = input("Enter student's first name: ")
    last_name = input("Enter student's last name: ")
    student_found = False
    for student, cls in students.items():
        if student[0] == first_name and student[1] == last_name:
            student_found = True
            print(f"\nClasses attended by {first_name} {last_name}:")
            for teacher, details in teachers.items():
                if cls in details['classes_taught']:
                    print(f"- {details['subject']} class by {teacher[0]} {teacher[1]}")
            break
    if not student_found:
        print("Student not found in the database.")

def manage_teacher(teachers):
    first_name = input("Enter teacher's first name: ")
    last_name = input("Enter teacher's last name: ")
    teacher_found = False
    for teacher, details in teachers.items():
        if teacher[0] == first_name and teacher[1] == last_name:
            teacher_found = True
            print(f"\nClasses taught by {first_name} {last_name}:")
            for cls in details['classes_taught']:
                print(f"- {cls}")
            break
    if not teacher_found:
        print("Teacher not found in the database.")

def manage_homeroom_teacher(homeroom_teachers, students):
    first_name = input("Enter homeroom teacher's first name: ")
    last_name = input("Enter homeroom teacher's last name: ")
    homeroom_teacher_found = False
    for teacher, cls in homeroom_teachers.items():
        if teacher[0] == first_name and teacher[1] == last_name:
            homeroom_teacher_found = True
            print(f"\nStudents led by {first_name} {last_name}:")
            for student, student_cls in students.items():
                if student_cls == cls:
                    print(f"- {student[0]} {student[1]}")
            break
    if not homeroom_teacher_found:
        print("Homeroom teacher not found in the database.")

def main():
    students = {}
    teachers = {}
    homeroom_teachers = {}

    while True:
        print("\nAvailable Commands:")
        print("1 - create - Create a new user")
        print("2 - manage - Manage users")
        print("3 - end - Terminate the program")

        command_input = input("Enter command by number or name: ").strip().lower()

        commands = {
            '1': 'create',
            '2': 'manage',
            '3': 'end'
        }

        if command_input in commands:
            command = commands[command_input]
        else:
            command = command_input

        if command == 'create':
            while True:
                print("\nUser Creation Process:")
                print("1 - student")
                print("2 - teacher")
                print("3 - homeroom teacher")
                print("4 - end")
                user_type_input = input("Enter user type to create by number or name: ").strip().lower()
                user_types = {
                    '1': 'student',
                    '2': 'teacher',
                    '3': 'homeroom teacher',
                    '4': 'end'
                }
                if user_type_input in user_types:
                    user_type = user_types[user_type_input]
                    if user_type == 'student':
                        create_student(students)
                    elif user_type == 'teacher':
                        create_teacher(teachers)
                    elif user_type == 'homeroom teacher':
                        create_homeroom_teacher(homeroom_teachers)
                    elif user_type == 'end':
                        break
                    else:
                        print("Invalid user type.")
                else:
                    print("Invalid user type.")
            continue

        elif command == 'manage':
            while True:
                print("\nUser Management Process:")
                print("1 - class")
                print("2 - student")
                print("3 - teacher")
                print("4 - homeroom teacher")
                print("5 - end")
                option_input = input("Enter option to manage by number or name: ").strip().lower()
                options = {
                    '1': 'class',
                    '2': 'student',
                    '3': 'teacher',
                    '4': 'homeroom teacher',
                    '5': 'end'
                }
                if option_input in options:
                    option = options[option_input]
                    if option == 'class':
                        manage_class(students, homeroom_teachers)
                    elif option == 'student':
                        manage_student(students, teachers)
                    elif option == 'teacher':
                        manage_teacher(teachers)
                    elif option == 'homeroom teacher':
                        manage_homeroom_teacher(homeroom_teachers, students)
                    elif option == 'end':
                        break
                    else:
                        print("Invalid option.")
                else:
                    print("Invalid option.")
            continue

        elif command == 'end':
            print("Exiting the program...")
            break

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
