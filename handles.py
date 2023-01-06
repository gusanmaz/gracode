import csv
import os


def get_students(csv_path):
    f = open(csv_path)
    r = csv.reader(f)

    students = dict()
    for row in r:
        new_student = {
            "id": row[0],
            "name": row[1],
            "surname": row[2]
        }
        students[row[0]] = new_student
    return students


def get_student_from_handle(students, handle):
    for id in students:
        stu = students[id]
        if 'handle' in stu and stu['handle'] == handle:
            return stu


def get_submitted_students(wd_path, students):
    codes_path = os.path.join(wd_path, "codes")
    listing = os.scandir(codes_path)
    for entry in listing:
        if entry.is_dir():
            user_dir = entry.name
            user_path = os.path.join(codes_path, user_dir)
            files = os.listdir(user_path)
            for file in files:
                if file.endswith('.txt') and file[:-4].isdigit() and len(file[:-4]) == 10:
                    student_no = file[:-4]
                    if student_no in students:
                        students[student_no]["handle"] = user_dir
    return students
