import networkx as nx
import matplotlib.pyplot as plt


def check_eulerian(graph):
    """Проверка, есть ли Эйлеров цикл (все степени четные)"""
    odd_degree_nodes = [v for v, d in graph.degree() if d % 2 != 0]
    if len(odd_degree_nodes) == 0:
        return True
    return False


def is_bridge(graph, u, v):
    """Проверка, является ли ребро (u, v) мостом"""
    # Если после удаления ребра количество компонент связности увеличивается - это мост
    original_components = nx.number_connected_components(graph)
    graph.remove_edge(u, v)
    new_components = nx.number_connected_components(graph)
    graph.add_edge(u, v)  # Возвращаем ребро обратно
    return new_components > original_components


def fleury_algorithm(graph):
    """Реализация алгоритма Флёри"""
    if not check_eulerian(graph):
        print("Граф не имеет Эйлерова цикла (есть вершины с нечетной степенью).")
        return None

    # Работаем с копией графа, чтобы не портить исходный
    g = graph.copy()
    # Начинаем с любой вершины
    start_node = list(g.nodes())[0]
    current_node = start_node
    path = [current_node]

    while g.number_of_edges() > 0:
        # Получаем всех соседей текущей вершины
        neighbors = list(g.neighbors(current_node))

        for neighbor in neighbors:
            # ПРАВИЛО ФЛЁРИ: Если это мост и есть альтернативы - пропускаем
            if is_bridge(g, current_node, neighbor) and len(neighbors) > 1:
                continue
            else:
                # Идём по ребру
                g.remove_edge(current_node, neighbor)
                current_node = neighbor
                path.append(current_node)
                break

    return path

def export_to_dot(graph, filename="graph.dot"):
    """
    Экспорт графа в формат DOT
    используем встроенную функцию networkx,
    которая генерирует правильный синтаксис
    """
    # Генерируем DOT-строку
    dot_data = nx.nx_pydot.to_pydot(graph).to_string()

    # Записываем в файл
    with open(filename, "w") as f:
        f.write(dot_data)
    print(f"Граф экспортирован в файл: {filename}")

# --- Пример работы ---
if __name__ == "__main__":


    G = nx.Graph()
    G.add_edges_from([
        ('A', 'B'), ('B', 'C'), ('C', 'A'),  # Треугольник 1
        ('C', 'D'), ('D', 'E'), ('E', 'C')  # Треугольник 2
    ])

    print("Степени вершин:", dict(G.degree()))

    euler_path = fleury_algorithm(G)
    print("Эйлеров цикл (путь):", euler_path)