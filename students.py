from utility import filter_by_field


def sort_students_by_name(students):
    students = filter_by_field(students, 'handle')
    sorted_people = sorted(students, key=lambda x: x['name'])
    return sorted_people


def sort_students_by_surname(students):
    students = filter_by_field(students, 'handle')
    sorted_people = sorted(students, key=lambda x: x['surname'])
    return sorted_people


def sort_students_by_handle(students):
    students = filter_by_field(students, 'handle')
    sorted_people = sorted(students, key=lambda x: x['handle'])
    return sorted_people


def sort_students_by_id(students):
    students = filter_by_field(students, 'handle')
    sorted_people = sorted(students, key=lambda x: x['id'])
    return sorted_people


