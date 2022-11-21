import csv
import re
import prettytable
from datetime import datetime


def check_for_empty_str(list):
    for item in list:
        if item == '' or item == 'None':
            return False
    return True


def clean_spaces(str):
    str = re.sub(r'\s+', ' ', str)
    str = str.strip()
    return str


def clean_html_tags(str):
    str = re.sub(r'<[^>]+>', '', str)
    return str


def csv_reader(file_name):
    list_naming = []
    with open(file_name, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        try:
            header = (next(reader))
        except StopIteration:
            return '', ''
        number_of_row = len(header)

        for row in reader:
            if len(row) == number_of_row and check_for_empty_str(row):
                list_naming.append(row)

    return header, list_naming


def csv_filer(header, list_naming):
    data_vacancies = []
    for name in list_naming:
        i = 0
        vacancy_dict = {}
        list_flag = False

        for string in name:
            if '\n' in string:
                splited_string = string.split('\n')
                list_flag = True

            if list_flag:
                cleaned_string = []
                for item in splited_string:
                    cleaned_string.append(clean_spaces(clean_html_tags(item)))
                list_flag = False
            else:
                cleaned_string = clean_spaces(clean_html_tags(string))

            vacancy_dict[header[i]] = cleaned_string
            i += 1

        data_vacancies.append(vacancy_dict)

    return data_vacancies


def format_num(num):
    num = int(float(num))
    str = f'{num:,}'
    return ' '.join(str.split(','))


def format_date(str):
    date = datetime.strptime(str, '%Y-%m-%dT%H:%M:%S%z')
    return date.__format__('%d.%m.%Y')


def format_salary(dict):
    salary_from = format_num(dict['Нижняя граница вилки оклада'])
    salary_to = format_num(dict['Верхняя граница вилки оклада'])
    dict_salary_gross = dict['Оклад указан до вычета налогов']
    if dict_salary_gross == 'Да':
        salary_gross = 'Без вычета налогов'
    elif dict_salary_gross == 'Нет':
        salary_gross = 'С вычетом налогов'
    salary_currency = dict['Идентификатор валюты оклада']

    salary = f'{salary_from} - {salary_to} ({salary_currency}) ({salary_gross})'

    new_dict = {}
    for key, value in dict.items():
        if key == 'Нижняя граница вилки оклада' or \
                key == 'Верхняя граница вилки оклада' or \
                key == 'Оклад указан до вычета налогов':
            pass
        elif key == 'Идентификатор валюты оклада':
            new_dict['Оклад'] = salary
        else:
            new_dict[key] = value

    return new_dict


def translate_dict(data, dict_naming):
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            if value in dict_naming:
                value = dict_naming[value]
        if key in dict_naming:
            key = dict_naming[key]
        translated_data[key] = value
    return translated_data


def formatter(data, dict_naming):
    formated_data = []
    for item in data:
        formated_dict = translate_dict(item, dict_naming)
        formated_dict = format_salary(formated_dict)
        formated_dict['Дата публикации вакансии'] = format_date(formated_dict['Дата публикации вакансии'])
        formated_data.append(formated_dict)
    return formated_data


def print_vacancies(data_vacancies, dict_naming, print_funcs, print_vars):
    i = 1
    end = len(data_vacancies)
    formated_data = formatter(data_vacancies, dict_naming)
    table = prettytable.PrettyTable()
    data_keys = list(formated_data[0].keys())
    table.field_names = ["№"] + data_keys
    table.align = 'l'
    width_dict = {}

    for key in data_keys:
        width_dict[key] = 20

    table._max_width = width_dict
    table.hrules = prettytable.ALL

    for item in formated_data:

        new_row = [i]

        for value in item.values():
            if isinstance(value, list):
                value = '\n'.join(value)
            if len(value) > 100:
                value = value[:100] + '...'
            new_row.append(value)
        table.add_row(new_row)
        i += 1

    print(print_funcs[print_vars['type']](print_vars, table))


def main():
    cells_ru = {'name': 'Название',
                'description': 'Описание',
                'key_skills': 'Навыки',
                'experience_id': 'Опыт работы',
                'premium': 'Премиум-вакансия',
                'employer_name': 'Компания',
                'salary': 'Оклад',
                'salary_from': 'Нижняя граница вилки оклада',
                'salary_to': 'Верхняя граница вилки оклада',
                'salary_gross': 'Оклад указан до вычета налогов',
                'salary_currency': 'Идентификатор валюты оклада',
                'area_name': 'Название области',
                'published_at': 'Дата публикации вакансии'}

    currencies_ru = {"AZN": "Манаты",
                     "BYR": "Белорусские рубли",
                     "EUR": "Евро",
                     "GEL": "Грузинский лари",
                     "KGS": "Киргизский сом",
                     "KZT": "Тенге",
                     "RUR": "Рубли",
                     "UAH": "Гривны",
                     "USD": "Доллары",
                     "UZS": "Узбекский сум"}

    experience_ru = {"noExperience": "Нет опыта",
                     "between1And3": "От 1 года до 3 лет",
                     "between3And6": "От 3 до 6 лет",
                     "moreThan6": "Более 6 лет"}

    bool_ru = {"true": "Да",
               "True": "Да",
               "TRUE": "Да",
               "false": "Нет",
               "False": "Нет",
               "FALSE": "Нет"}

    print_funcs = {
        '': lambda vars, table: table.get_string(start=vars['start'], end=vars['end'], fields=vars['fields']),
        'no start_end' : lambda vars, table: table.get_string(fields=vars['fields']),
        'no end': lambda vars, table: table.get_string(start=vars['start'], fields=vars['fields']),
        ' no fields': lambda vars, table: table.get_string(start=vars['start'], end=vars['end']),
        'no end no fields': lambda vars, table: table.get_string(start=vars['start']),
        'no start_end no fields': lambda vars, table: table}

    ru_dict = {**cells_ru, **currencies_ru, **experience_ru, **bool_ru}
    file_path = input()
    start_end_str = input()
    fields = input()

    print_vars = {'type': ''}
    if start_end_str == '':
        print_vars['type'] = 'no start_end'
    elif ' ' in start_end_str:
        print_vars['start'], print_vars['end'] = map(int, start_end_str.split())
        print_vars['start'] -= 1
    else:
        print_vars['start'] = int(start_end_str)
        print_vars['start'] -= 1
        print_vars['type'] = 'no end'

    if fields == '':
        print_vars['type'] = print_vars['type'] + ' no fields'
    else:
        print_vars['fields'] = ['№'] + fields.split(', ')


    header, list_naming = csv_reader(file_path)
    if header == '':
        print('Пустой файл')
    elif not list_naming:
        print('Нет данных')
    else:
        vacancies = csv_filer(header, list_naming)
        print_vacancies(vacancies, ru_dict, print_funcs, print_vars)


if __name__ == '__main__':
    main()