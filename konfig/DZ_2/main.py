import requests
import zipfile
import io
import graphviz
import argparse
from urllib.parse import urlparse

def get_dependencies(package_name):
    dependencies = set()
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
    
    if "message" in response:
        return dependencies
    
    version = response["info"]["version"]
    releases = response["releases"]
    latest_release = releases[version][0]
    urlWHL = latest_release["url"]

    WHLFile = requests.get(urlWHL)

    if urlWHL.endswith("tar.gz"):
        return dependencies

    zf = zipfile.ZipFile(io.BytesIO(WHLFile.content))

    metadata = ""
    for file in zf.namelist():
        if file.endswith("METADATA"):
            metadata = str(zf.read(file), "utf-8")
    lines = metadata.split("\n")

    for line in lines:
        if "Requires-Dist" in str(line):
            dependency = str(line).split(" ")
            if "extra" in dependency:
                break
            dependency = dependency[1].split("\\")[0]
            dependencies.add(dependency)
    return dependencies

def get_dependencies_github(repo_url, branch='main'):
    dependencies = set()
    try:
        # Construct URL for raw requirements.txt
        raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + f"/{branch}/requirements-dev.txt"
        
        # Get the content of the requirements.txt
        response = requests.get(raw_url)
        
        if response.status_code != 200:
            return dependencies

        requirements_content = response.text
        
        # Parse dependencies
        for line in requirements_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):  # Skip empty lines and comments
                dependencies.add(line.split("==")[0].strip())  # Get package name, ignore version

    except Exception as e:
        print(f"Error fetching dependencies: {e}")

    return dependencies

def format_dependencies_to_nested_dicts(main_package, dependencies, visited=None):
    if visited is None:
        visited = set()

    formatted_dependencies = {main_package: []}

    if dependencies is None:
        return formatted_dependencies

    visited.add(main_package)

    for dependency in dependencies:
        dependency = dependency.split(" ")
        package_name = dependency[0]

        if package_name in visited:
            continue

        visited.add(package_name)
        internal_dependencies = get_dependencies(package_name)
        formatted_internal_dependencies = format_dependencies_to_nested_dicts(
            package_name, internal_dependencies, visited
        )
        formatted_dependencies[main_package].append(formatted_internal_dependencies)

    return formatted_dependencies




def convertDicts(nested_dicts, depth, i):
    GraphCode = ""

    for key in nested_dicts:
        if not nested_dicts[key]:
            return f"\"{key}\";\n"
        
        for nested_dict in nested_dicts[key]:
            name = '"' + list(nested_dict.keys())[0].split('>')[0] + '";'
            GraphCode += f"\"{key}\"->{name}\n"
            
            if i < depth:
                dep = get_dependencies(list(nested_dict.keys())[0].split('>')[0])
                dependency_tree = format_dependencies_to_nested_dicts(list(nested_dict.keys())[0].split('>')[0], dep)
                links = convertDicts(dependency_tree, depth-i, 1)
                GraphCode += links
    
    return GraphCode

def render_graph(dot_code, output_file):
    graph = graphviz.Source(dot_code)
    graph.render(output_file, format='png', cleanup=True)
    print(f"Graph saved as {output_file}.png")

def main():
    parser = argparse.ArgumentParser(description="VM")
    parser.add_argument('--graphviz')
    parser.add_argument('--package')
    parser.add_argument('--output')
    parser.add_argument('--depth')
    parser.add_argument('--url')
    args = parser.parse_args()

    error_message = "Cannot get dependencies for this package"

    depth = int(args.depth)
    output = args.output
    if args.package:
        package_name = args.package
        if len(package_name) < 3:
            print(error_message)
        else:
            dependencies = get_dependencies(package_name)
            if dependencies:
                dependency_tree = format_dependencies_to_nested_dicts(package_name, dependencies)
                links = convertDicts(dependency_tree, depth, 1)
                graph_code = "digraph G {\n" + links + "}"
                render_graph(graph_code, output)
    elif args.url:
        package_url = args.url
        package_name = urlparse(package_url).path.strip("/").split("/")[1]
        if len(package_name) < 3:
            print(error_message)
        else:
            dependencies = get_dependencies_github(package_url)
            if dependencies:
                dependency_tree = format_dependencies_to_nested_dicts(package_name, dependencies)
                links = convertDicts(dependency_tree, depth, 1)
                graph_code = "digraph G {\n" + links + "}"
                render_graph(graph_code, output)
    else:
        print(error_message)

if __name__ == '__main__':
    main()