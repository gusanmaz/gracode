import csv
import glob
import os.path
import sys
from handles import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1);
    wd = sys.argv[1]
    p = os.path.join(wd, "*.csv")

    csv_files = glob.glob(p)
    #print(csv_files)

    data_csv_path = os.path.join(wd, "students.csv")
    students = get_students(data_csv_path)

    for file in csv_files:
        if "students.csv" in file:
            continue
        print(file)

    results_path = os.path.join(wd, "results.csv")
    results = open(results_path, "w")
    wr = csv.writer(results)
    header = ["id", "name", "surname"]
    files = []

    for file in csv_files:
        if "students.csv" in file:
            continue
        if "results.csv" in file:
            continue
        parts = os.path.split(file)
        header.append(parts[1])
        files.append(parts[1])

    for id, student in students.items():
        student['grades'] = [0] * len(files)

    ind = 0
    for file in csv_files:
        if "students.csv" in file:
            continue
        if "results.csv" in file:
            continue
        parts = os.path.split(file)
        header.append(parts[1])
        files.append(parts[1])
        f = open(file)
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                i = 1
                continue
            id = row[0]
            grade = row[-1]
            #curStudent = students[id]
            students[id]['grades'][ind] = int(grade)
            #students[id] = curStudent
        ind = ind + 1


    wr.writerow(header)
    for _, student in students.items():
        row = [student['id'], student['name'], student['surname']]
        row.extend(student['grades'])
        wr.writerow(row)
    results.close()




    results.close()


