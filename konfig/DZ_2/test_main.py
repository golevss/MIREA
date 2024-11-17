import unittest
from unittest.mock import patch, MagicMock
import main

class TestMain(unittest.TestCase):

    @patch('requests.get')
    def test_get_dependencies_success(self, mock_get):
        mock_response = {
            "info": {"version": "1.0.0"},
            "releases": {
                "1.0.0": [{
                    "url": "https://example.com/package-1.0.0.whl"
                }]
            }
        }
        mock_get.return_value.json.return_value = mock_response
        
        mock_whl_file = MagicMock()
        mock_whl_file.content = b"Mock file content"
        mock_get.return_value = mock_whl_file
        
        dependencies = main.get_dependencies('some-package')
        self.assertEqual(dependencies, set())

    @patch('requests.get')
    def test_get_dependencies_github(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'package1\npackage2==1.0.0\n#comment'
        mock_get.return_value = mock_response

        dependencies = main.get_dependencies_github('https://github.com/user/repo')
        self.assertEqual(dependencies, {'package1', 'package2'})

    @patch('main.get_dependencies')
    def test_format_dependencies_to_nested_dicts(self, mock_get_dependencies):
        mock_get_dependencies.side_effect = lambda package_name: {
            'package1': ['package2'],
            'package2': ['package3'],
            'package3': []
        }.get(package_name, [])

        main_package = 'package1'
        dependencies = ['package2']

        expected_result = {
            'package1': [
                {'package2': [
                    {'package3': []}
                ]}
            ]
        }

        result = main.format_dependencies_to_nested_dicts(main_package, dependencies)
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_convertDicts(self, mock_get):
        mock_get.return_value.json.return_value = {'info': {'version': '1.0.0'}, 'releases': {'1.0.0': [{'url': 'https://example.com/package-1.0.0.whl'}]}}
    
        mock_whl_file = MagicMock()
        mock_whl_file.content = b"Mock content of the WHL file"
        mock_get.return_value = mock_whl_file
    
        nested_dicts = {'main-package': [{'package1': {}}]}
        depth = 2
        graph_code = main.convertDicts(nested_dicts, depth, 1)
    
        self.assertIn('"main-package"->', graph_code)
        self.assertIn('"package1";', graph_code)

    @patch('graphviz.Source')
    def test_render_graph(self, mock_graphviz):
        mock_graphviz.return_value.render.return_value = 'test_output.png'

        dot_code = "digraph G {\n\"main-package\"->\"package1\";\n}"
        output_file = "test_output"
        main.render_graph(dot_code, output_file)
        
        mock_graphviz.return_value.render.assert_called_with(output_file, format='png', cleanup=True)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.get_dependencies')
    @patch('main.get_dependencies_github')
    @patch('main.render_graph')
    def test_main_function(self, mock_render_graph, mock_get_dependencies_github, mock_get_dependencies, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            **{
                'package': 'some-package',
                'url': None,
                'depth': 1,
                'output': 'output.png',
                'graphviz': None
            }
        )
        
        mock_get_dependencies.return_value = {'package1', 'package2'}

        main.main()

        mock_render_graph.assert_called_once()
        self.assertIn('output.png', str(mock_render_graph.call_args))

if __name__ == '__main__':
    unittest.main()
