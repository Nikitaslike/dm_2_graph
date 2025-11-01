import itertools
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit
)

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

def draw_graph(matrix, directed=False):
    """Візуалізація графа за матрицею"""
    G = nx.DiGraph() if directed else nx.Graph()
    n = len(matrix)
    G.add_nodes_from(range(1, n + 1))
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                if directed or (j > i):
                    G.add_edge(i + 1, j + 1)

    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, with_labels=True, node_color="#ffd280",
                     node_size=800, font_size=10, font_weight='bold',
                     edgecolors="black")
    title = "Орієнтований граф" if directed else "Неорієнтований граф"
    plt.title(title)
    plt.axis('off')
    plt.show()


def analyze_graph(matrix, directed=False, log=print):
    """Аналіз графа"""
    n = len(matrix)
    log("\n" + "=" * 60)
    log(f"АНАЛІЗ {'ОРІЄНТОВАНОГО' if directed else 'НЕОРІЄНТОВАНОГО'} ГРАФА")
    log("=" * 60)

    edges = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                if directed or (j > i):
                    edges.append((i + 1, j + 1))

    log(f"Вершини: {list(range(1, n + 1))}")
    log(f"Кількість ребер: {len(edges)}")
    log(f"Ребра: {edges}")

    log("\nОколиці вершин:")
    for i in range(n):
        neigh = [j + 1 for j in range(n) if matrix[i][j] != 0]
        degree = len(neigh)
        log(f"Вершина {i + 1}: околиця = {neigh}, степінь = {degree}")

    if not directed:
        all_even = all(sum(row) % 2 == 0 for row in matrix)
        log("\nЕйлерів цикл існує ✅" if all_even else "\nЕйлерового циклу немає ❌")

    def has_hamiltonian_cycle():
        for perm in itertools.permutations(range(n)):
            if all(matrix[perm[i]][perm[(i + 1) % n]] for i in range(n)):
                return [p + 1 for p in perm] + [perm[0] + 1]
        return None

    hc = has_hamiltonian_cycle()
    log("Гамільтонів цикл знайдено: " + str(hc) if hc else "Гамільтонового циклу не знайдено.")

    log("\nЦикли (до 4 вершин):")
    cycles = set()
    for a, b, c in itertools.permutations(range(n), 3):
        if matrix[a][b] and matrix[b][c] and matrix[c][a]:
            cycles.add(tuple(sorted([a + 1, b + 1, c + 1])))
    for cyc in list(cycles)[:5]:
        log(str(cyc))
    log("=" * 60)


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


# === PyQt5 GUI ===
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналіз графів та коди Прюфера — Варіант №14")
        self.resize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        buttons = QHBoxLayout()
        self.btn_a = QPushButton("Граф A (неорієнтований)")
        self.btn_b = QPushButton("Граф B (орієнтований)")
        self.btn_prufer = QPushButton("Декодувати коди Прюфера")
        buttons.addWidget(self.btn_a)
        buttons.addWidget(self.btn_b)
        buttons.addWidget(self.btn_prufer)
        layout.addLayout(buttons)
        self.setLayout(layout)

        self.btn_a.clicked.connect(self.show_a)
        self.btn_b.clicked.connect(self.show_b)
        self.btn_prufer.clicked.connect(self.show_prufer)

    def log(self, text):
        self.text_output.append(text)
        self.text_output.verticalScrollBar().setValue(
            self.text_output.verticalScrollBar().maximum()
        )

    def show_a(self):
        self.text_output.clear()
        analyze_graph(matrix_a, directed=False, log=self.log)
        draw_graph(matrix_a, directed=False)

    def show_b(self):
        self.text_output.clear()
        analyze_graph(matrix_b, directed=True, log=self.log)
        draw_graph(matrix_b, directed=True)

    def show_prufer(self):
        self.text_output.clear()
        self.log("=== ДЕКОДУВАННЯ КОДІВ ПРЮФЕРА ===\n")
        for name, code in codes.items():
            edges = prufer_decode(code)
            self.log(f"{name}) Код {code} → ребра {edges}")
            G = nx.Graph()
            G.add_edges_from(edges)
            plt.figure(figsize=(5, 5))
            nx.draw(G, with_labels=True, node_color="#b3ffb3",
                    node_size=700, edgecolors="black", font_weight="bold")
            plt.title(f"Граф з коду Прюфера {name}")
            plt.axis('off')
            plt.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())