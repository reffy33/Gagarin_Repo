import unittest
from main import format_salary


class TestFormatSalary(unittest.TestCase):

    def test_salary1(self):
        input = {'Нижняя граница вилки оклада': '10000',
                 'Верхняя граница вилки оклада': '100000',
                 'Идентификатор валюты оклада': 'RUR',
                 'Оклад указан до вычета налогов': 'Да'}
        output = {'Оклад': '10 000 - 100 000 (RUR) (Без вычета налогов)'}

        self.assertEqual(format_salary(input), output)

    def test_salary2(self):
        input = {'Нижняя граница вилки оклада': '200000',
                 'Верхняя граница вилки оклада': '500000',
                 'Идентификатор валюты оклада': 'USD',
                 'Оклад указан до вычета налогов': 'Нет'}
        output = {'Оклад': '200 000 - 500 000 (USD) (С вычетом налогов)'}

        self.assertEqual(format_salary(input), output)
