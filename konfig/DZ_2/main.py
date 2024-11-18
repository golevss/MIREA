import requests
import graphviz
import json
import argparse
from urllib.parse import urlparse

def get_dependencies(package_name):
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
    dependencies = response.get("info", {})["requires_dist"]
    return ",".join(dependencies).split(',')
    

def convertDicts(pack_name, dicts, depth, i):
    GraphCode = ""
    visited = set()
    for pack in dicts:
        name_pack = pack.split('>')[0]
        if name_pack in visited:
            pass
        else:
            GraphCode += f"\"{pack_name}\"->\"{name_pack}\"\n"
            visited.add(name_pack)
        
        if i < depth:
            print(name_pack)
            dependency_tree = get_dependencies(name_pack)
            links = convertDicts(name_pack,dependency_tree, depth-i, 1)
            GraphCode += links
    
    return GraphCode

def render_graph(dot_code, output_file):
    graph = graphviz.Source(dot_code)
    graph.render(output_file, format='png', cleanup=True)
    print(f"Graph saved as {output_file}.png")

def main():
    parser = argparse.ArgumentParser(description="Viz")
    parser.add_argument('--graphviz')
    parser.add_argument('--package')
    parser.add_argument('--output')
    parser.add_argument('--depth')
    parser.add_argument('--url')
    args = parser.parse_args()

    error_message = "Cannot get dependencies for this package"
    package_name = args.package
    output = args.output
    depth = int(args.depth)

    dependencies = get_dependencies(package_name)
    for pack in dependencies:
        print (pack.split('>')[0])

    links = convertDicts(package_name,dependencies, depth, 1)
    graph_code = "digraph G {\n" + links + "}"
    print(graph_code)
    render_graph(graph_code, output)

if __name__ == '__main__':
    main()