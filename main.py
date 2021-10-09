import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ

names_pattern = r"(([А-Я][а-я]+)(\s|\S)(([А-Я][а-я]+)(\s|\S)([А-Я][а-я]+)))|([А-Я][а-я]+)(\s)([А-Я][а-я]+)"
phone_number_pattern = r"(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})"

employees_list = {}
different_employees_list = {}

for i in contacts_list[1:]:
    try:
        text = ' '.join(i)
        name = re.match(names_pattern, text)
        number = r"+7 (\2) \3-\4-\5"
        if len(name.group().split()) == 2:
            lastname, firstname = name.group().split()
            i[0], i[1], i[2] = lastname, firstname, ''
        else:
            lastname, firstname, surname = name.group().split()
            i[0], i[1], i[2] = lastname, firstname, surname
        phone_number = re.sub(phone_number_pattern, r"+7(\2)\3-\4-\5", i[5])
        full_number = re.sub(r"\(*(доб.) (\d+)\)*", r"\1\2", i[5])
        full_number = re.sub(phone_number_pattern, r"+7(\2)\3-\4-\5", full_number)
        i[5] = full_number
        key = ''.join(i[0:2])
        if key in employees_list:
            different_employees_list[key] = i
        else:
            employees_list[key] = i
    except AttributeError:
        continue

for i in different_employees_list:
    if i in employees_list:
        for j in enumerate(employees_list[i]):
            if j[1] == '':
                employees_list[i][j[0]] = different_employees_list[i][j[0]]

employee_list_complete = [contacts_list[0]]

for employee in employees_list.values():
    employee_list_complete.append(employee)

# TODO 2: сохраните получившиеся данные в другой файл

with open("phonebook.csv", "w") as f:
    data_writer = csv.writer(f, delimiter=',')
    data_writer.writerows(employee_list_complete)
