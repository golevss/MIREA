import unittest
from unittest.mock import patch, MagicMock
import main

class TestMain(unittest.TestCase):

    @patch('requests.get')
    def test_get_dependencies_success(self, mock_get):
        # Mock the response from PyPI API
        mock_response = {
            "info": {"version": "1.0.0"},
            "releases": {
                "1.0.0": [{
                    "url": "https://example.com/package-1.0.0.whl"
                }]
            }
        }
        mock_get.return_value.json.return_value = mock_response
        
        # Mock the .whl file request
        mock_whl_file = MagicMock()
        mock_whl_file.content = b"Mock file content"
        mock_get.return_value = mock_whl_file
        
        # Test that the function returns the correct set of dependencies
        dependencies = main.get_dependencies('some-package')
        self.assertEqual(dependencies, set())  # In this case, the dependencies set should be empty

    @patch('requests.get')
    def test_get_dependencies_github(self, mock_get):
        # Mock the response for GitHub repository
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'package1\npackage2==1.0.0\n#comment'
        mock_get.return_value = mock_response

        # Test the dependencies fetched from GitHub
        dependencies = main.get_dependencies_github('https://github.com/user/repo')
        self.assertEqual(dependencies, {'package1', 'package2'})  # Ensure only the package names are added

    @patch('requests.get')
    def test_convertDicts(self, mock_get):
        # Mock the nested dependency structure
        mock_get.return_value.json.return_value = {'info': {'version': '1.0.0'}, 'releases': {'1.0.0': [{'url': 'https://example.com/package-1.0.0.whl'}]}}
    
        # Mock the response for the .whl file
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
        # Mock the rendering process
        mock_graphviz.return_value.render.return_value = 'test_output.png'

        dot_code = "digraph G {\n\"main-package\"->\"package1\";\n}"
        output_file = "test_output"
        main.render_graph(dot_code, output_file)
        
        # Check if the render method was called with the expected arguments
        mock_graphviz.return_value.render.assert_called_with(output_file, format='png', cleanup=True)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.get_dependencies')
    @patch('main.get_dependencies_github')
    @patch('main.render_graph')
    def test_main_function(self, mock_render_graph, mock_get_dependencies_github, mock_get_dependencies, mock_parse_args):
        # Set up a mock argument parser
        mock_parse_args.return_value = MagicMock(
            **{
                'package': 'some-package',
                'url': None,
                'depth': 1,
                'output': 'output.png',
                'graphviz': None
            }
        )
        
        # Mock the dependency retrieval
        mock_get_dependencies.return_value = {'package1', 'package2'}

        # Call the main function
        main.main()

        # Check if the render_graph function was called
        mock_render_graph.assert_called_once()
        self.assertIn('output.png', str(mock_render_graph.call_args))

if __name__ == '__main__':
    unittest.main()
