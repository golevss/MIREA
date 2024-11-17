import argparse
import subprocess
import sys
from pathlib import Path
from graphviz import Digraph


def fetch_dependencies(package_name):
    """
    Возвращает список зависимостей пакета.
    :param package_name: Имя пакета.
    :return: Список зависимостей.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("Requires:"):
                raw_deps = line.split(":")[1].strip()
                return raw_deps.split(", ") if raw_deps else []
        return []
    except subprocess.CalledProcessError:
        print(f"Не удалось получить информацию о пакете {package_name}.")
        return []


def resolve_transitive_dependencies(package_name, resolved=None, max_depth=None, current_depth=0):
    """
    Рекурсивно определяет транзитивные зависимости пакета до указанной глубины.
    
    :param package_name: Имя пакета.
    :param resolved: Множество разрешённых зависимостей.
    :param max_depth: Максимальная глубина обработки.
    :param current_depth: Текущая глубина рекурсии.
    :return: Множество уникальных имён зависимостей.
    """
    if resolved is None:
        resolved = set()

    # Ограничение глубины
    if max_depth is not None and current_depth >= max_depth:
        return resolved

    if package_name in resolved:
        return resolved

    resolved.add(package_name)
    dependencies = fetch_dependencies(package_name)

    for dep in dependencies:
        if dep not in resolved:
            resolve_transitive_dependencies(dep, resolved, max_depth, current_depth + 1)

    return resolved


def generate_dependency_graph(package_name, output_path, max_depth):
    """
    Генерирует граф зависимостей с помощью Graphviz.
    :param package_name: Имя основного пакета.
    :param output_path: Путь для сохранения графа.
    :param max_depth: Максимальная глубина зависимостей.
    """
    dependencies = resolve_transitive_dependencies(package_name, max_depth=max_depth)
    graph = Digraph(format="png")

    # Добавляем узлы в граф
    for dep in dependencies:
        graph.node(dep)

    # Связываем узлы
    for dep in dependencies:
        sub_deps = fetch_dependencies(dep)
        for sub_dep in sub_deps:
            if sub_dep in dependencies:  # Только если подзависимость включена в граф
                graph.edge(dep, sub_dep)

    # Сохраняем граф
    graph.render(output_path, cleanup=True)
    print(f"Граф зависимостей успешно сохранён в файл {output_path}.png")

    # Вывод названий пакетов на экран
    print("\nНайденные зависимости:")
    for dep in sorted(dependencies):
        print(dep)


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
        "--max-depth", type=int, required=False, default=None, help="Максимальная глубина зависимостей (по умолчанию без ограничений)"
    )

    args = parser.parse_args()

    # Устанавливаем путь к Graphviz
    graphviz_path = Path(args.graphviz_path)
    if not graphviz_path.exists():
        print(f"Указанный путь к Graphviz ({graphviz_path}) не существует.")
        sys.exit(1)

    # Выполняем визуализацию
    generate_dependency_graph(args.package_name, args.output_path, args.max_depth)


if __name__ == "__main__":
    main()
