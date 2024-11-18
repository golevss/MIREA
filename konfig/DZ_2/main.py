import requests
import graphviz
import argparse
import re

def get_dependencies(package_name):
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
    if "requires_dist" in response.get("info", {}):
        dependencies = response.get("info", {})["requires_dist"]
    else:
        return ""
    if dependencies == None:
        return ""
    return ",".join(dependencies).split(',')
    
vis = set()
def convertDicts(pack_name, dependencies, depth):
    if dependencies == "" or depth == 0:
        return f"\"{pack_name}\""
    
    GraphCode = ""
    visited = set()
    
    for pack in dependencies:
        match = re.match(r'^[a-zA-Z0-9_-]+',pack)
        if match:
            name_pack = pack[:match.end()]
        else:
            name_pack = pack
        
        if name_pack in visited or name_pack == "":
            pass
        else:
            if re.match(r'^[a-zA-Z0-9_-]+',name_pack) and name_pack != pack_name:
                GraphCode += f"\"{pack_name}\"->\"{name_pack}\"\n"
                visited.add(name_pack)
                vis.add(pack_name)
                print(name_pack, depth)
                if 1 < depth:
                    depth_pack = depth - 1
                    dependencies_pack = get_dependencies(name_pack)
                    GraphCode += convertDicts(name_pack, dependencies_pack, depth_pack)
    
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
    links = convertDicts(package_name,dependencies, depth)
    graph_code = "digraph G {\n" + links + "}"
    render_graph(graph_code, output)

if __name__ == '__main__':
    main()