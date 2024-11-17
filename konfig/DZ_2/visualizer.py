import argparse
import subprocess
import sys
from pathlib import Path
from graphviz import Digraph


def fetch_dependencies(package_name):
    """
    Возвращает словарь зависимостей пакета.
    Ключи — пакеты, значения — их зависимости.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        dependencies = {}
        for line in lines:
            if line.startswith("Requires:"):
                raw_deps = line.split(":")[1].strip()
                deps = raw_deps.split(", ") if raw_deps else []
                dependencies[package_name] = deps
        return dependencies
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении зависимостей для пакета {package_name}: {e}")
        sys.exit(1)


def resolve_transitive_dependencies(package_name, resolved=None, unresolved=None):
    """
    Рекурсивно определяет все транзитивные зависимости пакета.
    """
    if resolved is None:
        resolved = set()
    if unresolved is None:
        unresolved = set()

    if package_name in resolved:
        return resolved

    unresolved.add(package_name)
    deps = fetch_dependencies(package_name).get(package_name, [])

    for dep in deps:
        if dep not in resolved:
            resolve_transitive_dependencies(dep, resolved, unresolved)

    resolved.add(package_name)
    unresolved.remove(package_name)
    return resolved


def generate_dependency_graph(package_name, output_path):
    """
    Генерирует граф зависимостей с помощью Graphviz.
    """
    dependencies = resolve_transitive_dependencies(package_name)
    graph = Digraph(format="png")

    # Добавляем узлы и связи
    for dep in dependencies:
        sub_deps = fetch_dependencies(dep).get(dep, [])
        graph.node(dep)
        for sub_dep in sub_deps:
            graph.edge(dep, sub_dep)

    # Сохраняем граф
    graph.render(output_path, cleanup=True)
    print(f"Граф зависимостей успешно сохранён в файл {output_path}.png")


def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей Python-пакета")
    parser.add_argument(
        "--graphviz-path", type=str, required=True, help="Путь к программе для визуализации графов"
    )
    parser.add_argument(
        "--package-name", type=str, required=True, help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--output-path", type=str, required=True, help="Путь к файлу с изображением графа зависимостей"
    )
    parser.add_argument(
        "--repo-url", type=str, required=False, help="URL-адрес репозитория пакета"
    )

    args = parser.parse_args()

    # Устанавливаем путь к Graphviz
    graphviz_path = Path(args.graphviz_path)
    if not graphviz_path.exists():
        print(f"Указанный путь к Graphviz ({graphviz_path}) не существует.")
        sys.exit(1)

    # Выполняем визуализацию
    generate_dependency_graph(args.package_name, args.output_path)


if __name__ == "__main__":
    main()
