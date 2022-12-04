from datetime import datetime


def format_date_strptime(str):
    """
    Форматирует дату в формат ДД.ММ.ГГГГ
    :param str: (str) входная строка с датой
    :return: отформатированная дата
    >>> format_date_strptime('2022-07-15T09:56:52+0300')
    '15.07.2022'
    >>> format_date_strptime('2020-07-05T18:19:30+0300')
    '05.07.2020'
    >>> format_date_strptime('2022-07-18T01:14:25+0300')
    '18.07.2022'
    >>> format_date_strptime('2018-12-31T03:16:25+0300')
    '31.12.2018'
    """
    date = datetime.strptime(str, '%Y-%m-%dT%H:%M:%S%z')
    return date.__format__('%d.%m.%Y')


def format_date_as_string(str):
    """
    >>> format_date_as_string('2022-07-15T09:56:52+0300')
    '15.07.2022'
    >>> format_date_as_string('2020-07-05T18:19:30+0300')
    '05.07.2020'
    >>> format_date_as_string('2022-07-18T01:14:25+0300')
    '18.07.2022'
    >>> format_date_as_string('2018-12-31T03:16:25+0300')
    '31.12.2018'
    """
    return '.'.join(reversed(str[:10].split('-')))


def format_date_parcing_the_str(str):
    """
    >>> format_date_parcing_the_str('2022-07-15T09:56:52+0300')
    '15.07.2022'
    >>> format_date_parcing_the_str('2020-07-05T18:19:30+0300')
    '05.07.2020'
    >>> format_date_parcing_the_str('2022-07-18T01:14:25+0300')
    '18.07.2022'
    >>> format_date_parcing_the_str('2018-12-31T03:16:25+0300')
    '31.12.2018'
    """
    str = str[:10]
    year, month, day = map(int, str.split('-'))
    date = datetime(year, month, day)
    return date.__format__('%d.%m.%Y')


def main():
    date_list = ['2022-07-15T09:56:52+0300', '2020-07-05T18:19:30+0300', '2018-12-31T03:16:25+0300',
                 '2017-12-31T03:16:25+0300', '2017-11-30T03:16:25+0300', '2020-12-13T03:16:27+0300',
                 '2018-12-31T03:16:25+0300', '2018-11-30T03:16:25+0300', '2021-12-13T03:16:27+0300']

    # format_date_strptime
    for date in date_list:
        print(format_date_strptime(date))

    print()

    # format_date_as_string
    for date in date_list:
        print(format_date_as_string(date))

    print()

    # format_date_parcing_the_str
    for date in date_list:
        print(format_date_parcing_the_str(date))


if __name__ == '__main__':
    main()
