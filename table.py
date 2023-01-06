import json
import os.path
from tabulate import tabulate
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import anoymize


def get_html_table(data, students, results_path, hidden=True, num_chars_beginning=1, num_chars_end=1, hidden_char='*'):
    header = ["Öğrenci No", "İsim", "Soyisim", "Github Handle", "Repo URL"]
    header_titles = ["Öğrenci No", "İsim", "Soyisim", "Github Handle", "Repo URL"]

    rows = list()
    titles = header_titles

    stu_result_path = os.path.join(results_path, "gusanmaz" + ".json")
    stu_result_file = open(stu_result_path, "r")
    stu_result = json.load(stu_result_file)

    for task in stu_result['tasks']:
        header.append(task['name'] + "(" + str(task['points']) + "p)")
        task_title = "Expected stdout:{out}\nExpected stderr:{err}\nExpected timeout status:{timeout}\n".format(out=task['out'], err=task['err'], timeout=task['timeout'])
        titles.append(task_title)

    header.append("Total Points")
    titles.append("Total Points")
    rows.append(header)

    github_repo = data['githubRepo']
    project_dir = data['projectDir']
    url_prefix = "https://github.com"
    url_codes_masked = "tree/main/docs/codes/masked"
    url_codes_unmasked = "tree/main/docs/codes/unmasked"
    url_beginning = os.path.join(url_prefix, github_repo)
    student_urls = []
    handles = []

    for student in students:
        handle = student['handle']
        stu_result_path = os.path.join(results_path, handle + ".json")
        stu_result_file = open(stu_result_path, "r")
        stu_result = json.load(stu_result_file)

        id = anoymize.anonymize_name(stu_result['studentID'], hidden)
        name = anoymize.anonymize_name(stu_result['studentName'], hidden)
        surname = anoymize.anonymize_name(stu_result['studentSurname'], hidden)
        handle = anoymize.anonymize_name(handle, hidden)

        hidden_handle = anoymize.anonymize_name(handle, True)
        non_hidden_handle = anoymize.anonymize_name(handle, False)

        url = ""
        if hidden:
            url = os.path.join(url_prefix, github_repo, url_codes_masked, project_dir, handle)
            handles.append(hidden_handle)
        else:
            url = os.path.join(url_prefix, github_repo, url_codes_unmasked, project_dir, handle)
            handles.append(non_hidden_handle)
        student_urls.append(url)

        row = [id, name, surname, handle, url]
        titles.extend((id, name, surname, handle, "URL of folder with codes for project."))

        total_points = 0
        for task in stu_result['tasks']:
            if task['pass']:
                row.append("✅")
            else:
                row.append("❌")
            total_points += task['points']

            out = task['out']
            err = task['err']

            if len(out) > 1000:
                out = "stdout cok uzun. Bu testin tam stdout ciktisini gormek icin ilgili kullanicinin JSON dosyasini inceleyeniz."
            if len(err) > 1000:
                err = "stderr cok uzun. Bu testin tam stderr ciktisini gormek icin ilgili kullanicinin JSON dosyasini inceleyeniz."

            task_title = "stdout:{out}\nstderr:{err}\nTimeout Status:{timeout}\n".format(out=out, err=err, timeout=task['timeout'])
            titles.append(task_title)
        row.append(total_points)
        titles.append(total_points)
        rows.append(row)
    html_table = tabulate(rows, tablefmt='html')

    soup = BeautifulSoup(html_table)
    elems = soup.find_all("td")

    title_ind = 0
    for td in elems:
        td.attrs["title"] = titles[title_ind]
        title_ind += 1

    titled_table = soup.prettify()

    soup2 = BeautifulSoup(titled_table)
    for td in soup2.find_all('td'):
        if  url_beginning in td.text:
            url = student_urls.pop(0)
            handle = handles.pop(0)
            a = soup2.new_tag('a', url)
            a.string = handle
            a['href'] = url

            td.clear()
            td.append(a)
    titled_table = soup2.prettify()

    return titled_table


def write_table(path, html):
    f = open(path, "w")
    f.write(html)
    f.close()
