import os
import matplotlib.pyplot as plt

def student_grade():
    name = input("What is the student's name: ")
    with open('data/students.txt', 'r') as file:
        for line in file:
            if name in line:
                student_id = line[:3]
                if student_id.isdigit() and len(student_id) == 3:
                    break
                else:
                    print("Student not found.")
                    return

    total_points = 0
    for file in os.listdir('data/submissions'):
        with open(os.path.join('data/submissions', file), 'rb') as f:
            if f.read(3).decode() == student_id:
                f.seek(4)
                assignment_id = f.read(5).decode().strip()
                if not assignment_id.isdigit():  # Handle 4-digit IDs
                    f.seek(4)
                    assignment_id = f.read(4).decode().strip()
                f.seek(-2, 2)
                assignment_grade = int(f.read(2).decode().strip())
                with open('data/assignments.txt', 'r') as weights_file:
                    lines = weights_file.readlines()
                    for i in range(1, len(lines), 3):
                        if assignment_id == lines[i].strip():
                            assignment_weight = float(lines[i + 1].strip())
                            total_points += ((assignment_grade) / 100) * int(assignment_weight)
                            break
    
    percent_grade = round(total_points / 10)
    print(f"{percent_grade}%")

def assignment_statistics():
    assignment_name = input("What is the assignment name: ")
    with open('data/assignments.txt', 'r') as file:
        lines = file.readlines()
        assignment_id = None
        for i in range(0, len(lines), 3):
            if assignment_name == lines[i].strip():
                assignment_id = lines[i + 1].strip()
                break
    if assignment_id is None:
        print("Assignment not found.")
        return
    grades = []
    for file in os.listdir('data/submissions'):
        with open(os.path.join('data/submissions', file), 'r') as f:
            content = f.read()
            if f"|{assignment_id}|" in content:
                grade = content.split(f"|{assignment_id}|")[1][:2]
                grades.append(int(grade))
    if grades:
        average_grade = sum(grades) / len(grades)
        print(f"Min: {min(grades)}%")
        print(f"Avg: {average_grade:.1f}%")
        print(f"Max: {max(grades)}%")
    else:
        print(f"No grades found for {assignment_name}")

def assignment_graph():
    assignment_name = input("What is the assignment name: ")
    with open('data/assignments.txt', 'r') as file:
        lines = file.readlines()
        assignment_id = None
        for i in range(0, len(lines), 3):
            if assignment_name == lines[i].strip():
                assignment_id = lines[i + 1].strip()
                break
    if assignment_id is None:
        print("Assignment not found.")
        return
    grades = []
    for file in os.listdir('data/submissions'):
        with open(os.path.join('data/submissions', file), 'r') as f:
            content = f.read()
            if f"|{assignment_id}|" in content:
                grade = content.split(f"|{assignment_id}|")[1][:2]
                grades.append(int(grade))
    if grades:
        plt.hist(grades, bins=15, edgecolor='black')
        plt.title(f'Grade Distribution for {assignment_name}')
        plt.xlabel('Grades')
        plt.ylabel('Frequency')
        plt.show()
    else:
        print(f"No grades found for {assignment_name}")

def main():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")
    choice = input("Enter your selection: ")
    if choice == "1":
        student_grade()
    elif choice == "2":
        assignment_statistics()
    elif choice == "3":
        assignment_graph()

if __name__ == "__main__":
    main()
