import requests
import zipfile
import io
import graphviz
import argparse


# Get the dependencies of a package
def get_dependencies(package_name):
    # Set to store the dependencies
    dependencies = set()
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()

    # If the package does not exist, return an empty set
    if "message" in response:
        return dependencies

    version = response["info"]["version"]
    releases = response["releases"]
    latest_release = releases[version][0]
    urlWHL = latest_release["url"]

    WHLFile = requests.get(urlWHL)

    # Skip if file name ends with tar.gz
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
            # Remove the version number
            dependency = dependency[1].split("\\")[0]
            dependencies.add(dependency)
    return dependencies


# Format the dependencies to nested dictionaries
def format_dependencies_to_nested_dicts(main_package, dependencies):
    # Format: {main_package: [{dependency: [{dependency: []}]}]}
    formatted_dependencies = {main_package: []}

    if dependencies is None:
        return formatted_dependencies

    for dependency in dependencies:
        dependency = dependency.split(" ")
        # Skip if dependency is a link
        if dependency == main_package:
            continue
        if "extra" not in dependency:
            package_name = dependency[0]
            internal_dependencies = get_dependencies(package_name)
            formatted_internal_dependencies = format_dependencies_to_nested_dicts(package_name, internal_dependencies)
            formatted_dependencies[main_package].append(formatted_internal_dependencies)
    return formatted_dependencies


# Convert the nested dictionaries to graph code
def convertDicts(nested_dicts, depth, i):
    GraphCode = ""
    for key in nested_dicts:
        if not nested_dicts[key]:
            return f"\"{key}\";\n"
        for nested_dict in nested_dicts[key]:
            # If the depth is reached, return the key
            if i >= depth:
                if i + 1 < depth:
                    return f"\"{key}\"->{convertDicts(nested_dict, depth, i + 1)}"
                else:
                    return f"\"{key}\"\n"
            GraphCode += f"\"{key}\"->{convertDicts(nested_dict, depth, i + 1)}"
    return GraphCode

def render_graph(dot_code, output_file):
    graph = graphviz.Source(dot_code)
    graph.render(output_file, format='png', cleanup=True)
    print(f"Graph saved as {output_file}.png")

# Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="VM")
    parser.add_argument('--graphviz', help="Path to the filesystem archive.")
    parser.add_argument('--package', help="Path to the filesystem archive.")
    parser.add_argument('--output', help="Path to the filesystem archive.")
    parser.add_argument('--depth', help="Path to the filesystem archive.")
    args = parser.parse_args()

    error_message = "Cannot get dependencies for this package"    
    package_name = args.package
    depth = int(args.depth)
    output = args.output

    if len(package_name) < 3:
        print(error_message)
    else:        
        dependencies = get_dependencies(package_name)
        if dependencies:
            dependency_tree = format_dependencies_to_nested_dicts(package_name, dependencies)
            links = convertDicts(dependency_tree, depth, 0)
            graph_code = "digraph G {\n" + links + "}"
            #print(graph_code)
            render_graph(graph_code, output)
        else:
            print(error_message)