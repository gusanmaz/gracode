import csv
import json
import os.path
import io
from tabulate import tabulate

import anoymize


def get_csv_table(students, results_path, hidden=True, num_chars_beginning=1, num_chars_end=1, hidden_char='*'):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    header = ["Öğrenci No", "İsim", "Soyisim", "Github Handle"]

    rows = list()

    stu_result_path = os.path.join(results_path, "gusanmaz" + ".json")
    stu_result_file = open(stu_result_path, "r")
    stu_result = json.load(stu_result_file)

    for task in stu_result['tasks']:
        header.append(task['name'])
    header.append("Total Points")
    writer.writerow(header)

    for student in students:
        handle = student['handle']
        stu_result_path = os.path.join(results_path, handle + ".json")
        stu_result_file = open(stu_result_path, "r")
        stu_result = json.load(stu_result_file)

        id = anoymize.anonymize_name(stu_result['studentID'], hidden)
        name = anoymize.anonymize_name(stu_result['studentName'], hidden)
        surname = anoymize.anonymize_name(stu_result['studentSurname'], hidden)
        handle = anoymize.anonymize_name(handle, hidden)

        row = [id, name, surname, handle]

        totalPoints = 0
        for task in stu_result['tasks']:
            row.append(task['points'])
            totalPoints += task['points']
        row.append(totalPoints)
        writer.writerow(row)

    return output.getvalue()


def write_csv_table(path, csv):
    f = open(path, "w")
    f.write(csv)
    f.close()
