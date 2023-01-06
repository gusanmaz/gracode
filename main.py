import subprocess
import sys
import table
import shutil

from handles import *
from utility import *
from students import *
from csv_table import *
from funcs import *  # Run-time usage


def run_script(script_path, repo_path, arg):
    o = subprocess.run([script_path, repo_path, arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout_status = False
    if o.returncode == 124:
        timeout_status = True
    return {"out": o.stdout.decode(errors="ignore"),
            "err": o.stderr.decode(errors="ignore"),
            "timeout_status": timeout_status}


def write_script_output(out, out_path, err_path, timeout_path):
    dir_path = os.path.dirname(out_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    f = open(out_path, "w")
    f.write(out["out"])
    f.close()

    f = open(err_path, "w")
    f.write(out["err"])
    f.close()

    if out['timeout_status']:
        print("Timeout happens! for {path}".format(path=out_path))
        f = open(timeout_path, "w")
        f.write("Command timed out!")
        f.close()


def get_results(wd, data, students):
    outputs_path = os.path.join(wd, 'outputs')
    results_path = os.path.join(wd, 'results')
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    handles = get_dirs(outputs_path, full=False)
    reference_user = data['referenceUser']
    reference_path = os.path.join(outputs_path, reference_user)
    for handle in handles:
        handle_path = os.path.join(outputs_path, handle)
        student = get_student_from_handle(students, handle)

        if student is not None:
            result = {
                'projectName': data['name'],
                'studentName': student['name'],
                'studentSurname': student['surname'],
                'studentID': student['id']
            }
            task_results = list()
            for task in data['tasks']:
                test_name = task['testName']
                if test_name == "copy":
                    continue
                dotless_path = os.path.join(handle_path, test_name)
                out_path = os.path.join(dotless_path + ".out")
                err_path = os.path.join(dotless_path + ".err")
                timeout_path = os.path.join(dotless_path + ".timeout")

                dotless_path = os.path.join(reference_path, test_name)
                ref_out_path = os.path.join(dotless_path + ".out")
                ref_err_path = os.path.join(dotless_path + ".err")
                task_function = task['function']

                out = read_file(out_path)
                err = read_file(err_path)
                ref_out = read_file(ref_out_path)
                ref_err = read_file(ref_err_path)

                evalStr = '{func}("""{ref_out}""","""{ref_err}""","""{out}""","""{err}""")'.format(func=task_function,
                                                                                                   ref_out=ref_out,
                                                                                                   ref_err=ref_err,
                                                                                                   out=out, err=err)
                pass_status = eval(evalStr)

                print("Pass status for {user}-task#{test_name}: {pass_status}".format(user=handle, test_name=test_name,
                                                                                      pass_status=pass_status))

                task_result = {
                    "name": test_name,
                    "out": out,
                    "err": err,
                    "ref_out": ref_out,
                    "ref_err": ref_err,
                    "pass": pass_status,
                    "points": 0,
                    "timeout": False
                }

                if pass_status:
                    task_result['points'] = task['point']
                if os.path.exists(timeout_path):
                    task_result['timeout'] = True

                task_results.append(task_result)
            result['tasks'] = task_results

            json_path = os.path.join(results_path, handle + ".json")
            with open(json_path, "w") as json_file:
                json.dump(result, json_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1);
    wd = sys.argv[1]

    evaluate = True
    produce_report = True
    copy_codes = True
    copy_hidden = True
    produce_table = True

    gracode_path = os.path.join(wd, "gracode.json")
    evaluator_script_path = os.path.join(wd, 'commands.sh')
    copy_script_path = os.path.join(wd, 'copy.sh')
    codes_path = os.path.join(wd, 'codes')

    f = open(gracode_path)
    gracode = json.load(f)
    f.close()

    copy_dir = gracode['copyDir']
    copy_path = os.path.join(wd, copy_dir)

    copy_dir_hidden = gracode['copyDir'] + "_hidden"
    hidden_copy_path = os.path.join(wd, copy_dir_hidden)
    results_path = os.path.join(wd, "results")

    user_dirs = []
    with os.scandir(codes_path) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.name.startswith('.'):
                user_dirs.append(entry)

    students_data_path = os.path.join(wd, "students.csv")
    students = get_students(students_data_path)
    submitted_students = get_submitted_students(wd, students)

    if evaluate:
        if not os.path.exists(copy_path):
            os.makedirs(copy_path)

        for user_dir in user_dirs:
            print("Running test for user: {}".format(user_dir.name))
            for task in gracode['tasks']:
                task_name = task['testName']
                extensionless_path = os.path.join(wd, "outputs", user_dir.name, task_name)
                out_path = os.path.join(extensionless_path + ".out")
                err_path = os.path.join(extensionless_path + ".err")
                timeout_path = os.path.join(extensionless_path + ".timeout")
                script_out = run_script(evaluator_script_path, user_dir.path, task_name)
                write_script_output(script_out, out_path, err_path, timeout_path)

    # Produce JSON
    if produce_report:
        get_results(wd, gracode, students)

    # Copy files
    if copy_codes:
        for user_dir in user_dirs:
            print("Copying codes of user {}".format(user_dir.name))
            user_copy_path = os.path.join(copy_path, user_dir.name)
            if not os.path.exists(user_copy_path):
                os.makedirs(user_copy_path)
            script_out = run_script(copy_script_path, user_dir.path, user_copy_path)
            extensionless_path = os.path.join(wd, "outputs", user_dir, "copy")
            out_path = os.path.join(extensionless_path + ".out")
            err_path = os.path.join(extensionless_path + ".err")
            timeout_path = os.path.join(extensionless_path + ".timeout")
            write_script_output(script_out, out_path, err_path, timeout_path)

    # Hidden Copy

    if copy_hidden:
        if not os.path.exists(hidden_copy_path):
            os.makedirs(hidden_copy_path)

        with os.scandir(copy_path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.name.startswith('.'):
                    handle = entry.name
                    hidden_handle = anoymize.anonymize_name(handle, True)
                    hidden_handle_path = os.path.join(hidden_copy_path, hidden_handle)
                    if not os.path.exists(hidden_handle_path):
                        os.makedirs(hidden_handle_path)
                    json_filename = handle + ".json"
                    hidden_json_filename = hidden_handle + ".json"
                    json_path = os.path.join(results_path, json_filename)
                    hidden_json_path = os.path.join(hidden_handle_path, hidden_json_filename)
                    if os.path.exists(json_path):
                        shutil.copy(json_path, hidden_json_path)
                    main_path = os.path.join(copy_path, handle, "main.c")
                    hidden_main_path = os.path.join(hidden_copy_path, hidden_handle, "main.c")
                    if os.path.exists(main_path):
                        shutil.copy(main_path, hidden_main_path)

    # Create table
    if produce_table:
        students_list = dict_to_list(submitted_students)
        sorted_students = sort_students_by_id(students_list)
        results_path = os.path.join(wd, "results")

        html_hidden = table.get_html_table(gracode, sorted_students, results_path, True)
        hidden_results_html_path = os.path.join(wd, "table_hidden.html")
        table.write_table(hidden_results_html_path, html_hidden)

        html = table.get_html_table(gracode, sorted_students, results_path, False)
        results_html_path = os.path.join(wd, "table.html")
        table.write_table(results_html_path, html)

        csv_hidden = get_csv_table(sorted_students, results_path, True)
        hidden_results_html_path = os.path.join(wd, "table_hidden.csv")
        write_csv_table(hidden_results_html_path, csv_hidden)

        csv = get_csv_table(sorted_students, results_path, False)
        results_csv_path = os.path.join(wd, "table.csv")
        write_csv_table(results_csv_path, csv)
