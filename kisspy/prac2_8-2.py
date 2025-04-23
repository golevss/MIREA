import os
import argparse

def generate_tree(path):
    def walk_directory(directory):
        tree = []
        for root, dirs, files in os.walk(directory):
            depth = root.count(os.sep)
            current_directory = root.split(os.sep)[-1]
            tree.append(f"{'  ' * depth}{current_directory}/")
            for file in files:
                tree.append(f"{'  ' * (depth + 1)}{file}")
        return tree

    graph = ["digraph G {"]
    for entry in walk_directory(path):
        graph.append(f"  \"{entry}\";")
    graph.append("}")
    return "\n".join(graph)

def main():
    parser = argparse.ArgumentParser(description="Generate a directory tree in Graphviz format")
    parser.add_argument("path", nargs="?", default=".", help="Path to start the directory tree")
    
    args = parser.parse_args()
    
    tree = generate_tree(args.path)
    print(tree)

if __name__ == "__main__":
    main()
