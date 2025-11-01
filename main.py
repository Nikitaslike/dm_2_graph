import itertools
import subprocess
import sys

required = ["networkx", "matplotlib", "PyQt5"]
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QIcon

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

theory_text = """
📘 ТЕОРІЯ
─────────────────────────────
Основи графів
Граф — це множина вершин і ребер, які їх з’єднують. 
Ступінь вершини d(v) — кількість ребер, інцидентних вершині. 
Околиця вершини N(v) — множина суміжних вершин. 
Матриця суміжності — квадратна матриця, де 1 означає наявність ребра. 

Ланцюги, маршрути, цикли
Маршрут — послідовність вершин і ребер.
Ланцюг — маршрут без повторення ребер.
Цикл — замкнений ланцюг.

Ейлерові графи
Граф має ейлерів цикл тоді й лише тоді, коли всі вершини мають парний ступінь.
Якщо дві вершини непарні — існує ейлерів ланцюг.

Гамільтонові графи
Гамільтонів цикл проходить через усі вершини один раз.
Існує лише якщо граф зв’язний і має достатню кількість ребер.

Дерева та коди Прюфера
Дерево — це зв’язний граф без циклів.
Код Прюфера кодує дерево з n вершин у послідовність довжини n−2.
─────────────────────────────
"""

def draw_graph(matrix, directed=False):
    G = nx.DiGraph() if directed else nx.Graph()
    n = len(matrix)
    G.add_nodes_from(range(1, n + 1))
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                if directed or j > i:
                    G.add_edge(i + 1, j + 1)
    plt.figure(figsize=(6, 6), num="Граф A" if not directed else "Граф Б")
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, with_labels=True,
                     node_color="#ffd280" if not directed else "#b3d9ff",
                     node_size=800, font_size=10, font_weight="bold",
                     edgecolors="black")
    plt.title("Орієнтований граф" if directed else "Неорієнтований граф")
    plt.axis('off')
    plt.show()

def analyze_graph(matrix, directed=False, log=print):
    n = len(matrix)
    log(f"\n=== {'ОРІЄНТОВАНИЙ' if directed else 'НЕОРІЄНТОВАНИЙ'} ГРАФ ===")
    edges = [(i+1,j+1) for i in range(n) for j in range(n)
             if matrix[i][j] and (directed or j>i)]
    log(f"Вершини: {list(range(1, n+1))}")
    log(f"Кількість ребер: {len(edges)}")
    log(f"Ребра: {edges}")
    for i in range(n):
        neigh = [j+1 for j in range(n) if matrix[i][j]]
        log(f"Вершина {i+1}: околиця={neigh}, степінь={len(neigh)}")

    even = all(sum(row)%2==0 for row in matrix)
    log("Ейлерів цикл існує ✅" if even else "Ейлерового циклу немає ❌")

    def has_hamiltonian_cycle():
        for perm in itertools.permutations(range(n)):
            if all(matrix[perm[i]][perm[(i+1)%n]] for i in range(n)):
                return [p+1 for p in perm]+[perm[0]+1]
        return None

    hc = has_hamiltonian_cycle()
    log("Гамільтонів цикл: "+str(hc) if hc else "Гамільтонового циклу не знайдено.")

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

# codes = {
#     "a": [1,2,5,2,3,6],
#     "b": [8,2,7,3,4,1],
#     "c": [1,1,2,6,7,4,1],
#     "d": [5,11,8,4,2,2,1,3,9,10,13]
# }

code_a = [1,2,5,2,3,6]
code_b = [8,2,7,3,4,1]
code_c = [1,1,2,6,7,4,1]
code_d = [5,11,8,4,2,2,1,3,9,10,13]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Контрольна робота: Графи (Варіант 14)")
        self.setWindowIcon(QIcon())
        self.resize(950, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        self.text.append("Кр з дискретної математики")
        self.text.append("Тема: Графи\nВаріант №14")
        self.text.append("Студент: Мірошниченко Нікіта, 24ПР1")

        btns = QHBoxLayout()
        for name, func in [
            ("№1 Граф а", self.show_a),
            ("№1 Граф б", self.show_b),
            ("№4 Коди Прюфера", self.show_prufer),
            ("Теорія", self.show_theory)
        ]:
            b = QPushButton(name)
            b.clicked.connect(func)
            btns.addWidget(b)
        layout.addLayout(btns)
        self.setLayout(layout)

    def log(self, msg): self.text.append(msg)

    def show_a(self):
        self.text.clear()
        analyze_graph(matrix_a, False, log=self.log)
        draw_graph(matrix_a, False)
    def show_b(self):
        self.text.clear()
        analyze_graph(matrix_b, True, log=self.log)
        draw_graph(matrix_b, True)
    def show_prufer(self):
        self.text.clear()
        self.log("ДЕКОДУВАННЯ КОДІВ ПРЮФЕРА")

        all_codes = {
            "a": code_a,
            "b": code_b,
            "c": code_c,
            "d": code_d
        }

        for name, code in all_codes.items():
            edges = prufer_decode(code)
            self.log(f"{name}) {code} → {edges}")
            G = nx.Graph()
            G.add_edges_from(edges)
            plt.figure(figsize=(4, 4), num=f"Дерево з коду {name}")
            nx.draw(G, with_labels=True,
                    node_color="#b3ffb3",
                    node_size=700,
                    edgecolors="black")
            plt.title(f"Дерево з коду {name}")
            plt.show()
    def show_theory(self):
        self.text.clear()
        self.text.setPlainText(theory_text)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())