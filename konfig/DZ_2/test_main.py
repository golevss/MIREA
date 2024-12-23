import unittest
from unittest.mock import patch, MagicMock

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
    def test_get_dependencies_2(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "info": {
                "requires_dist": []
            }
        }
        mock_get.return_value = mock_response
        
        package_name = "some_package"
        result = get_dependencies(package_name)
        
        self.assertEqual(result, [''])
        mock_get.assert_called_once_with(f'https://pypi.org/pypi/{package_name}/json')

    @patch('requests.get')
    def test_get_dependencies_3(self, mock_get):
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

    @patch('requests.get')
    def test_get_dependencies_git_2(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        numpy
        -some_dependency
        """
        mock_get.return_value = mock_response
        
        package_url = "https://example.com/some_repo"
        result = get_dependencies_git(package_url)
        
        self.assertEqual(result, {'numpy'})
        mock_get.assert_called_once_with(package_url)

    def test_convertDicts(self):
        dependencies = ['numpy']
        package_name = "example_package"
        depth = 3
        result = convertDicts(package_name, dependencies, depth)
        
        self.assertIn('"example_package"->"numpy"', result)

    def test_convertDicts_2(self):
        dependencies = ['pack1!=1.6.5', 'pack2>=1.5.6', ' ', 'pack3>=1.5.6']
        package_name = "head_pack"
        depth = 2
        result = convertDicts(package_name, dependencies, depth)
        
        self.assertIn('"head_pack"->"pack1"', result)
        self.assertIn('"head_pack"->"pack2"', result)
        self.assertIn('"head_pack"->"pack3"', result)

    def test_convertDicts_3(self):
        dependencies = ['pack1!=1.6.5', 'pack2>=1.5.6', ' ', 'pack3>=1.5.6']
        package_name = "head_pack"
        depth = 0
        result = convertDicts(package_name, dependencies, depth)
        
        self.assertIn('"head_pack"', result)
    
    @patch('graphviz.Source.render')
    def test_render_graph(self, mock_render):
        dot_code = 'digraph G { "A"->"B"; }'
        output_file = 'output_graph'
        
        render_graph(dot_code, output_file)
        
        mock_render.assert_called_once_with(output_file, format='png', cleanup=True)

    @patch('graphviz.Source.render')
    def test_render_graph_2(self, mock_render):
        dot_code = 'digraph G { "A"->"B";"B"->"C"; }'
        output_file = 'output_graph'
        
        render_graph(dot_code, output_file)
        
        mock_render.assert_called_once_with(output_file, format='png', cleanup=True)

    @patch('graphviz.Source.render')
    def test_render_graph_3(self, mock_render):
        dot_code = 'digraph G { "A"; }'
        output_file = 'output_graph'
        
        render_graph(dot_code, output_file)
        
        mock_render.assert_called_once_with(output_file, format='png', cleanup=True)


if __name__ == '__main__':
    unittest.main()