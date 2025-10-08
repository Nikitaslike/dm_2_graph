import itertools

matrix_a = [
    [0,1,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [0,0,0,0,1,0,0,0,1,0],
    [1,1,0,0,0,0,1,1,0,1],
    [0,0,1,0,0,1,1,0,1,1],
    [0,0,0,0,1,0,0,1,1,0],
    [1,1,0,1,1,0,0,0,0,0],
    [0,0,0,1,0,1,0,0,1,1],
    [0,0,1,0,1,1,0,1,0,0],
    [1,1,0,1,1,0,0,1,0,0]
]

matrix_b = [
    [0,0,1,0,0,0,1,0,0,0],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,1,0],
    [0,1,0,0,0,0,1,1,0,1],
    [0,1,0,0,1,1,0,0,0,1],
    [0,0,0,0,1,0,0,1,1,0],
    [0,1,0,1,0,0,0,0,0,0],
    [0,0,0,1,0,1,0,0,1,1],
    [0,0,1,0,0,1,0,0,0,0],
    [0,1,0,1,1,0,0,0,0,1]
]

def analyze_graph(matrix, directed=False):
    n = len(matrix)
    print("\n" + "="*60)
    print(f"АНАЛІЗ {'ОРІЄНТОВАНОГО' if directed else 'НЕОРІЄНТОВАНОГО'} ГРАФА")
    print("="*60)

    # список ребер
    edges = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                if directed or (j > i):
                    edges.append((i+1, j+1))

    print(f"Вершини: {list(range(1, n+1))}")
    print(f"Кількість ребер: {len(edges)}")
    print(f"Ребра: {edges}")

    # степені та околиці
    print("\nОколиці вершин:")
    for i in range(n):
        neigh = [j+1 for j in range(n) if matrix[i][j] != 0]
        degree = len(neigh)
        print(f"Вершина {i+1}: околиця = {neigh}, степінь = {degree}")

    # ейлерів цикл (для неорієнтованого графа)
    if not directed:
        all_even = all(sum(row) % 2 == 0 for row in matrix)
        if all_even:
            print("\nЕйлерів цикл існує ✅")
        else:
            print("\nЕйлерового циклу немає ❌")

    # гамільтонів цикл
    def has_hamiltonian_cycle():
        for perm in itertools.permutations(range(n)):
            valid = True
            for i in range(n):
                a, b = perm[i], perm[(i+1) % n]
                if matrix[a][b] == 0:
                    valid = False
                    break
            if valid:
                return [p+1 for p in perm] + [perm[0]+1]
        return None

    hc = has_hamiltonian_cycle()
    if hc:
        print("Гамільтонів цикл знайдено:", hc)
    else:
        print("Гамільтонового циклу не знайдено.")

    # пошук простих циклів (до 4 вершин)
    print("\nЦикли (до 4 вершин):")
    cycles = set()
    for a, b, c in itertools.permutations(range(n), 3):
        if matrix[a][b] and matrix[b][c] and matrix[c][a]:
            cycles.add(tuple(sorted([a+1,b+1,c+1])))
    for cyc in list(cycles)[:5]:
        print(cyc)
    print("="*60)


# === Запуск аналізу ===

analyze_graph(matrix_a, directed=False)
analyze_graph(matrix_b, directed=True)


# === 3. Код Прюфера ===

def prufer_decode(code):
    m = len(code)
    n = m + 2
    vertices = list(range(1, n + 1))
    degree = {i: 1 for i in vertices}
    for x in code:
        degree[x] += 1
    edges = []
    for x in code:
        for v in sorted(vertices):
            if degree[v] == 1:
                edges.append((v, x))
                degree[v] -= 1
                degree[x] -= 1
                break
    u, v = [i for i in vertices if degree[i] == 1]
    edges.append((u, v))
    return edges


codes = {
    "a": [1,2,5,2,3,6],
    "b": [8,2,7,3,4,1],
    "c": [1,1,2,6,7,4,1],
    "d": [5,11,8,4,2,2,1,3,9,10,13]
}

print("\n\n=== ДЕКОДУВАННЯ КОДІВ ПРЮФЕРА ===")
for name, code in codes.items():
    edges = prufer_decode(code)
    print(f"{name}) Код Прюфера {code} -> ребра {edges}")