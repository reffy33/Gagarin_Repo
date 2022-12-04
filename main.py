import csv
import re
import prettytable
from datetime import datetime


def check_for_empty_str(list):
    """
    Проверяет список на отсутствие пустых строк
    :param list: (list) Список для проверки
    :return: bool: True если в списке нет пустых строк, False если они есть
    >>> check_for_empty_str(['123', 123, ''])
    False
    >>> check_for_empty_str(['', '', ''])
    False
    >>> check_for_empty_str([123, 123, '54234', '56 56'])
    True
    >>> check_for_empty_str(['', 'string', 'number'])
    False
    >>> check_for_empty_str(['empty', 'empty string'])
    True

    """
    for item in list:
        if item == '' or item == 'None':
            return False
    return True


def clean_spaces(str):
    """
    Отчищает строку от лишних пробельных символов
    :param str: (str) входная строка
    :return: str: отчищенная от лишних пробелов строка
    >>> clean_spaces(' word ')
    'word'
    >>> clean_spaces('  word  ')
    'word'
    >>> clean_spaces('correct string')
    'correct string'
    >>> clean_spaces('incorrect  string')
    'incorrect string'
    >>> clean_spaces('  a    lot    of     spaces ')
    'a lot of spaces'
    """
    str = re.sub(r'\s+', ' ', str)
    str = str.strip()
    return str


def clean_html_tags(str):
    """
    Отчищает строку от html тэгов типа <тэг>
    :param str: (str) входная строка
    :return: str: строка очищенная от html тэгов

    >>> clean_html_tags('Text without html tags')
    'Text without html tags'
    >>> clean_html_tags('Do not detele this &nbsp')
    'Do not detele this &nbsp'
    >>> clean_html_tags('<b>Delete this please</b>')
    'Delete this please'
    >>> clean_html_tags('</a>Why this tag is closed before opened?<a>')
    'Why this tag is closed before opened?'
    >>> clean_html_tags('<a></a><html></b></br><button>')
    ''
    """
    str = re.sub(r'<[^>]+>', '', str)
    return str


def csv_reader(file_name):
    """
    Считывает данные из csv файла
    :param file_name: (str) путь до файла
    :return: header (list): список содержащий заголовки
    :return: list_naming (list): список которых хранит в себе последующие строки csv файла в виде списков
    """
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
    """
    Создаёт список из словарей вакансий, в котором ключом является заголовок столбца,
    а значение - содержимым строки с этим заголовком
    :param header: (list) список заголовков
    :param list_naming: (list) список строк
    :return: list: данные о вакансиях
    """
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
    """
    Форматирует сумма с пробелом в качестве разделителя
    например 10.000 --> 10 000
    :param num: (str) входная строка
    :return str: отфоматированная сумма

    >>> format_num('1')
    '1'
    >>> format_num('100')
    '100'
    >>> format_num('10000')
    '10 000'
    >>> format_num('100000')
    '100 000'
    >>> format_num('1000000')
    '1 000 000'
    """
    num = int(float(num))
    str = f'{num:,}'
    return ' '.join(str.split(','))


def format_date(str):
    """
    Форматирует дату в формат ДД.ММ.ГГГГ
    :param str: (str) входная строка с датой
    :return: отформатированная дата
    >>> format_date('2022-07-15T09:56:52+0300')
    '15.07.2022'
    >>> format_date('2020-07-05T18:19:30+0300')
    '05.07.2020'
    >>> format_date('2022-07-18T01:14:25+0300')
    '18.07.2022'
    >>> format_date('2018-12-31T03:16:25+0300')
    '31.12.2018'
    """
    date = datetime.strptime(str, '%Y-%m-%dT%H:%M:%S%z')
    return date.__format__('%d.%m.%Y')


def format_salary(dict):
    """
    Форматирует поля зарплаты в словаре в формат
    [Сумма от] - [Сумма до] ([валюта оклада]) Без вычета налогов/С вычетом налогов
    :param dict: (dict) входной словарь
    :return dict: словарь с отформатированными полями с зарплатой
    """
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
    """
    Переводит данные в словаре на русский с помощью словаря dict_naming
    :param data: (dict) входной словарь с данными на русском
    :param dict_naming: (dict) словарь формата {'фраза на английском' : 'фраза на русском'}
    :return: dict: переведённый словарь
    """
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
    """
    Вспомогательная функция, переводит словарь на русский, форматирует поля с зарплатой и датами,
    с помощью функций translate_dict, format_salary, format_date
    :param data: (list[dict]) входные данные, требующие форматирования
    :param dict_naming: (dict) словарь для перевода фраз на русский
    :return: list[dict]: отформатированные данные
    """
    formated_data = []
    for item in data:
        formated_dict = translate_dict(item, dict_naming)
        formated_dict = format_salary(formated_dict)
        formated_dict['Дата публикации вакансии'] = format_date(formated_dict['Дата публикации вакансии'])
        formated_data.append(formated_dict)
    return formated_data


def print_vacancies(data_vacancies, dict_naming, print_funcs, print_vars):
    """
    Форматирует данные о вакансиях, выводит из в таблицу с помощью библиотеки PrettyTables
    :param data_vacancies: (list[dict]) данные о вакансиях
    :param dict_naming: (dict) словарь для перевода фраз на русский
    :param print_funcs: (dict[str : lambda]) словарь содержащий лямбда функции для печати таблицы
    и их краткое словестное описание
    Например:
    'no start_end': lambda vars, table: table.get_string(fields=vars['fields']

    :param print_vars: (dict) словарь описывающий параметры печати
    обязательный ключ type - возможные значения:
    'no start_end no fields' - печать определённых столбцов таблицы и всех строк
    'no start_end' - печать определённых столбцов таблицы и всех строк
    'no end' - печать определённых столбцов таблицы, начиная с определённой строки и до конца таблицы
    ' no fields' - печать всех столбцов таблицы, начиная и заканчивая на определённой строке
    'no end no fields' - печать всех столбцов таблицы, начиная с определённой строки и до конца таблицы
    '' -  печать определённых столбцов таблицы, начиная и заканчивая на определённой строке

    необязательные ключи
    'start' - строка с которой нужно начать печать таблицы
    'end' - конечная строка которой нужно закончить печать таблицы (только при наличии ключа 'start')
    'fields' - список столбцов которые нужно печатать
    """
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
    """
    Создаёт необходимые словари: для перевода фраз на русский, словарь содержащий лямбда функции для печати таблицы,
    словарь описывающий параметры печати, считывает информацию от пользователя, вызывает print_vacancies для печати
    """
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
                'area_name': 'Название штата',
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
        'no start_end': lambda vars, table: table.get_string(fields=vars['fields']),
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
