import unittest
from unittest.mock import patch, MagicMock
import graphviz
import requests
import re

from main import get_dependencies, get_dependencies_git, convertDicts, render_graph

class TestPackageDependencies(unittest.TestCase):

    @patch('requests.get')
    def test_get_dependencies(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "info": {
                "requires_dist": ["numpy", "requests"]
            }
        }
        mock_get.return_value = mock_response
        
        package_name = "some_package"
        result = get_dependencies(package_name)
        
        self.assertEqual(result, ['numpy', 'requests'])
        mock_get.assert_called_once_with(f'https://pypi.org/pypi/{package_name}/json')

    @patch('requests.get')
    def test_get_dependencies_no_requires_dist(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "info": {}
        }
        mock_get.return_value = mock_response
        
        package_name = "some_package"
        result = get_dependencies(package_name)
        
        self.assertEqual(result, "")
        mock_get.assert_called_once_with(f'https://pypi.org/pypi/{package_name}/json')

    @patch('requests.get')
    def test_get_dependencies_git(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        numpy
        requests
        -some_dependency
        """
        mock_get.return_value = mock_response
        
        package_url = "https://example.com/some_repo"
        result = get_dependencies_git(package_url)
        
        self.assertEqual(result, {'numpy', 'requests'})
        mock_get.assert_called_once_with(package_url)

    def test_convertDicts(self):
        dependencies = ['numpy', 'requests']
        package_name = "example_package"
        depth = 2
        result = convertDicts(package_name, dependencies, depth)
        
        self.assertIn('"example_package"->"numpy"', result)
        self.assertIn('"example_package"->"requests"', result)
    
    @patch('graphviz.Source.render')
    def test_render_graph(self, mock_render):
        dot_code = 'digraph G { "A"->"B"; }'
        output_file = 'output_graph'
        
        render_graph(dot_code, output_file)
        
        mock_render.assert_called_once_with(output_file, format='png', cleanup=True)

if __name__ == '__main__':
    unittest.main()