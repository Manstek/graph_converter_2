from collections import defaultdict, deque
from .models import Vertex, Edge


def find_hierarchical_levels():
    vertices = Vertex.objects.all()
    num_vertices = vertices.count()
    in_degree = {vertex.id: 0 for vertex in vertices}
    levels = defaultdict(list)

    # Считаем входящие рёбра
    edges = Edge.objects.all()
    for edge in edges:
        in_degree[edge.to_vertex.id] += 1

    # Находим вершины 0 уровня
    queue = deque([vertex.id for vertex in vertices if in_degree[vertex.id] == 0])

    level = 0

    while queue:
        current_level_size = len(queue)

        for _ in range(current_level_size):
            current = queue.popleft()
            levels[level].append(current)

            # Уменьшаем входящие рёбра у соседей
            for edge in edges.filter(from_vertex_id=current):
                in_degree[edge.to_vertex.id] -= 1
                if in_degree[edge.to_vertex.id] == 0:
                    queue.append(edge.to_vertex.id)

        level += 1

    return levels
