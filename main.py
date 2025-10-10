import itertools
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

def analyze_graph(matrix, directed=False):
    n = len(matrix)
    log("\n" + "="*60)
    log(f"АНАЛІЗ {'ОРІЄНТОВАНОГО' if directed else 'НЕОРІЄНТОВАНОГО'} ГРАФА")
    log("="*60)

    # список ребер
    edges = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                if directed or (j > i):
                    edges.append((i+1, j+1))

    log(f"Вершини: {list(range(1, n+1))}")
    log(f"Кількість ребер: {len(edges)}")
    log(f"Ребра: {edges}")

    # степені та околиці
    log("\nОколиці вершин:")
    for i in range(n):
        neigh = [j+1 for j in range(n) if matrix[i][j] != 0]
        degree = len(neigh)
        log(f"Вершина {i+1}: околиця = {neigh}, степінь = {degree}")

    # ейлерів цикл (для неорієнтованого графа)
    if not directed:
        all_even = all(sum(row) % 2 == 0 for row in matrix)
        if all_even:
            log("\nЕйлерів цикл існує ✅")
        else:
            log("\nЕйлерового циклу немає ❌")

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
        log("Гамільтонів цикл знайдено: " + str(hc))
    else:
        log("Гамільтонового циклу не знайдено.")

    # пошук простих циклів (до 4 вершин)
    log("\nЦикли (до 4 вершин):")
    cycles = set()
    for a, b, c in itertools.permutations(range(n), 3):
        if matrix[a][b] and matrix[b][c] and matrix[c][a]:
            cycles.add(tuple(sorted([a+1,b+1,c+1])))
    for cyc in list(cycles)[:5]:
        log(str(cyc))
    log("="*60)


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

# GUI

# root = tk.Tk()
# root.title("Аналіз графів та декодування кодів Прюфера")

# text_output = scrolledtext.ScrolledText(root, width=100, height=30, wrap=tk.WORD)
# text_output.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


# PyQt5 GUI
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналіз графів та коди Прюфера")
        self.resize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setLineWrapMode(QTextEdit.WidgetWidth)
        layout.addWidget(self.text_output)

        button_layout = QHBoxLayout()
        self.btn_a = QPushButton("Аналізувати граф A")
        self.btn_b = QPushButton("Аналізувати граф B")
        self.btn_prufer = QPushButton("Декодувати коди Прюфера")
        button_layout.addWidget(self.btn_a)
        button_layout.addWidget(self.btn_b)
        button_layout.addWidget(self.btn_prufer)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.btn_a.clicked.connect(self.analyze_a)
        self.btn_b.clicked.connect(self.analyze_b)
        self.btn_prufer.clicked.connect(self.decode_prufer)

    def log(self, msg):
        self.text_output.append(msg)
        self.text_output.verticalScrollBar().setValue(self.text_output.verticalScrollBar().maximum())

    def analyze_a(self):
        self.text_output.clear()
        analyze_graph(matrix_a, directed=False, log=self.log)

    def analyze_b(self):
        self.text_output.clear()
        analyze_graph(matrix_b, directed=True, log=self.log)

    def decode_prufer(self):
        self.text_output.clear()
        self.log("\n\n=== ДЕКОДУВАННЯ КОДІВ ПРЮФЕРА ===")
        for name, code in codes.items():
            edges = prufer_decode(code)
            self.log(f"{name}) Код Прюфера {code} -> ребра {edges}")


# Patch analyze_graph to accept log as argument
def analyze_graph(matrix, directed=False, log=print):
    n = len(matrix)
    log("\n" + "="*60)
    log(f"АНАЛІЗ {'ОРІЄНТОВАНОГО' if directed else 'НЕОРІЄНТОВАНОГО'} ГРАФА")
    log("="*60)

    # список ребер
    edges = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                if directed or (j > i):
                    edges.append((i+1, j+1))

    log(f"Вершини: {list(range(1, n+1))}")
    log(f"Кількість ребер: {len(edges)}")
    log(f"Ребра: {edges}")

    # степені та околиці
    log("\nОколиці вершин:")
    for i in range(n):
        neigh = [j+1 for j in range(n) if matrix[i][j] != 0]
        degree = len(neigh)
        log(f"Вершина {i+1}: околиця = {neigh}, степінь = {degree}")

    # ейлерів цикл (для неорієнтованого графа)
    if not directed:
        all_even = all(sum(row) % 2 == 0 for row in matrix)
        if all_even:
            log("\nЕйлерів цикл існує ✅")
        else:
            log("\nЕйлерового циклу немає ❌")

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
        log("Гамільтонів цикл знайдено: " + str(hc))
    else:
        log("Гамільтонового циклу не знайдено.")

    # пошук простих циклів (до 4 вершин)
    log("\nЦикли (до 4 вершин):")
    cycles = set()
    for a, b, c in itertools.permutations(range(n), 3):
        if matrix[a][b] and matrix[b][c] and matrix[c][a]:
            cycles.add(tuple(sorted([a+1,b+1,c+1])))
    for cyc in list(cycles)[:5]:
        log(str(cyc))
    log("="*60)


# PyQt5 application launcher
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())