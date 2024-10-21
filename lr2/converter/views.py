from django.shortcuts import render
from collections import defaultdict
from .forms import IncidenceMatrixForm


def convert_incidence_matrix(matrix):
    vertices_count = len(matrix)
    edges_count = len(matrix[0])
    adjacency_matrix = [[0] * vertices_count for _ in range(vertices_count)]

    for j in range(edges_count):
        start_vertex = end_vertex = None
        for i in range(vertices_count):
            if matrix[i][j] == 1:
                start_vertex = i
            elif matrix[i][j] == -1:
                end_vertex = i
        if start_vertex is not None and end_vertex is not None:
            adjacency_matrix[start_vertex][end_vertex] = 1

    return adjacency_matrix


def find_hierarchical_levels(adjacency_matrix):
    num_vertices = len(adjacency_matrix)
    levels = defaultdict(list)

    # Находим вершины 0 уровня (где все входящие рёбра равны 0)
    zero_level = [i for i in range(num_vertices) if all(adjacency_matrix[j][i] == 0 for j in range(num_vertices))]
    levels[0].extend(zero_level)

    # Переменная для хранения текущего уровня
    current_level = zero_level

    level = 1

    while current_level:
        next_level = set()  # Используем set для уникальности

        for vertex in current_level:
            # Проверяем все вершины, которые могут зависеть от текущей
            for neighbor in range(num_vertices):
                if adjacency_matrix[vertex][neighbor] == 1:
                    next_level.add(neighbor)

        # Фильтруем только те вершины, которые ещё не были добавлены в уровни
        next_level = [v for v in next_level if v not in sum(levels.values(), [])]

        if next_level:
            levels[level].extend(next_level)

        current_level = next_level
        level += 1

    # Преобразуем индексы в удобный формат
    for i in levels:
        levels[i] = [v + 1 for v in levels[i]]  # +1 для удобства отображения

    return levels


def create_adjacency_matrix_from_levels(levels, original_matrix):
    old_to_new = {}
    new_vertices = []

    # Создание отображения старых вершин в новые
    for level in levels.values():
        for vertex in level:
            if vertex not in old_to_new:
                old_to_new[vertex] = len(new_vertices) + 1
                # Нумерация начинается с 1
                new_vertices.append(vertex)

    new_vertex_count = len(new_vertices)
    new_adjacency_matrix = [[0] * new_vertex_count for _ in range(new_vertex_count)]

    # Заполнение новой матрицы смежности
    for level_index in range(len(levels) - 1):
        current_level = levels[level_index]
        next_level = levels[level_index + 1]

        for vertex in current_level:
            for neighbor in next_level:
                if original_matrix[vertex - 1][neighbor - 1] == 1:
                    new_adjacency_matrix[old_to_new[vertex] - 1][old_to_new[neighbor] - 1] = 1

    return new_adjacency_matrix, old_to_new


def matrix_view(request):
    if request.method == 'POST':
        form = IncidenceMatrixForm(request.POST)
        if form.is_valid():
            matrix_input = form.cleaned_data['matrix']
            matrix = [list(map(int, row.split())) for row in matrix_input.strip().split('\n')]
            adjacency_matrix = convert_incidence_matrix(matrix)
            levels = find_hierarchical_levels(adjacency_matrix)
            new_adj_matrix, old_to_new = create_adjacency_matrix_from_levels(levels, adjacency_matrix)
            levels_template = []
            for level, ver in dict(levels).items():
                string = f'{level} уровень - {ver}'
                levels_template.append(string)
            return render(request,
                          'levels.html',
                          {'levels': levels_template,
                           'adjacency_matrix': adjacency_matrix,
                           'new_adj_matrix': new_adj_matrix,
                           'old_to_new': old_to_new})
    else:
        form = IncidenceMatrixForm()

    return render(request, 'matrix_input.html', {'form': form})

# matrix = [
#     [0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0],
#     [1, 0, 0, 0, 1, 0, 1],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 1, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 0, 1, 0, 0, 0],
# ]
# смежность
# matrix_2 = [
#     [1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [-1, 0, -1, 0, 0, 1, -1, 0, 0, 0],
#     [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, -1, 1, -1],
#     [0, 0, 1, -1, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, -1, 0, 0, -1, 0],
#     [0, 0, 0, 0, -1, 0, 1, 0, 0, 1]
# ]
# инциденция
