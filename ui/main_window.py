import os
import subprocess
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QFileDialog,
    QVBoxLayout, QWidget, QAction, QToolBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("C Quick IDE")
        self.setGeometry(100, 100, 900, 600)

        self.current_file = ""

        # Editor
        self.editor = QTextEdit()
        self.editor.setStyleSheet("background:#1e1e1e; color:white;")

        # Output Panel
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(150)
        self.output.setStyleSheet("background:#111; color:#00ff00;")

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_toolbar()
        self.create_shortcuts()

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        create_action = QAction(QIcon("assets/create.png"), "New", self)
        create_action.triggered.connect(self.new_file)
        toolbar.addAction(create_action)

        open_action = QAction(QIcon("assets/create.png"), "Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction(QIcon("assets/create.png"), "Save", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        compile_action = QAction(QIcon("assets/compile.png"), "Compile", self)
        compile_action.triggered.connect(self.compile_code)
        toolbar.addAction(compile_action)

        run_action = QAction(QIcon("assets/run.png"), "Run", self)
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)

    def create_shortcuts(self):
        self.editor.setFocus()

        save_shortcut = QAction(self)
        save_shortcut.setShortcut("Ctrl+S")
        save_shortcut.triggered.connect(self.save_file)
        self.addAction(save_shortcut)

        open_shortcut = QAction(self)
        open_shortcut.setShortcut("Ctrl+O")
        open_shortcut.triggered.connect(self.open_file)
        self.addAction(open_shortcut)

        run_shortcut = QAction(self)
        run_shortcut.setShortcut("F5")
        run_shortcut.triggered.connect(self.compile_and_run)
        self.addAction(run_shortcut)

    def new_file(self):
        self.editor.clear()
        self.current_file = ""

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open C File", "", "C Files (*.c)"
        )
        if filename:
            with open(filename, "r") as f:
                self.editor.setText(f.read())
            self.current_file = filename

    def save_file(self):
        if not self.current_file:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "C Files (*.c)"
            )
            if filename:
                self.current_file = filename
        if self.current_file:
            with open(self.current_file, "w") as f:
                f.write(self.editor.toPlainText())

    def compile_code(self):
        if not self.current_file:
            return
        result = subprocess.run(
            ["gcc", self.current_file, "-o", "a.out"],
            capture_output=True, text=True
        )
        self.output.setText(result.stderr or "Compiled Successfully")

    def run_code(self):
        result = subprocess.run(
            ["./a.out"],
            capture_output=True, text=True
        )
        self.output.append(result.stdout)

    def compile_and_run(self):
        self.compile_code()
        self.run_code()