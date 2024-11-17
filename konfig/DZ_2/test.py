import unittest
from unittest.mock import patch, MagicMock
import requests
import io
import zipfile
import graphviz

from main import get_dependencies, format_dependencies_to_nested_dicts, convertDicts, render_graph


class TestDependencyGraph(unittest.TestCase):

    @patch('requests.get')
    def test_get_dependencies(self, mock_get):
        # Симуляция ответа от PyPI для пакета
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'info': {'version': '1.0.0'},
            'releases': {'1.0.0': [{'url': 'http://example.com/package-1.0.0.whl'}]}
        }

        # Мокаем поведение requests.get для возврата этого ответа
        mock_get.return_value = mock_response

        # Симуляция содержимого WHL файла
        whl_file_content = io.BytesIO(b'PK\x03\x04')  # Минимальный действительный контент для тестирования
        with patch('requests.get', return_value=MagicMock(content=whl_file_content)):
            dependencies = get_dependencies('mock_package')

        # Проверяем, что список зависимостей правильно заполняется
        self.assertEqual(dependencies, set())

    def test_format_dependencies_to_nested_dicts(self):
        # Мокированные данные
        dependencies = ["dep1", "dep2"]
        
        # Ожидаемый результат
        expected_result = {
            "mock_package": [
                {"dep1": []},
                {"dep2": []}
            ]
        }

        # Запуск функции
        result = format_dependencies_to_nested_dicts("mock_package", dependencies)

        # Проверка результата
        self.assertEqual(result, expected_result)

    def test_convertDicts(self):
        # Тестирование простой вложенной структуры
        nested_dicts = {
            "mock_package": [
                {"dep1": []},
                {"dep2": []}
            ]
        }

        # Ожидаемый Graphviz DOT код
        expected_output = "\"mock_package\"->\"dep1\";\n\"mock_package\"->\"dep2\";\n"

        # Запуск функции
        result = convertDicts(nested_dicts, 1, 0)

        # Проверка результата
        self.assertEqual(result, expected_output)

    @patch('graphviz.Source.render')
    def test_render_graph(self, mock_render):
        # Мокированный Graphviz dot код
        dot_code = "digraph G {\"mock_package\"->\"dep1\";}"

        # Вызов функции render_graph (она должна вызвать graphviz.Source.render)
        render_graph(dot_code, 'output_test')

        # Проверка, что метод render был вызван с правильными аргументами
        mock_render.assert_called_once_with('output_test', format='png', cleanup=True)


if __name__ == '__main__':
    unittest.main()