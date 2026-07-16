from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QProgressBar,
    QTextEdit,
    QFileDialog,
)

from core.logger import Logger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sabbir AI Studio")
        self.resize(1200, 800)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Title
        title = QLabel("Sabbir AI Bulk Image Generator")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            padding:10px;
        """)
        layout.addWidget(title)

        # ---------------- Prompt File ----------------

        prompt_layout = QHBoxLayout()

        prompt_label = QLabel("Prompt File:")

        self.prompt_path = QLineEdit()
        self.prompt_path.setPlaceholderText("Select Prompt File...")

        self.browse_prompt = QPushButton("Browse")
        self.browse_prompt.clicked.connect(self.select_prompt_file)

        prompt_layout.addWidget(prompt_label)
        prompt_layout.addWidget(self.prompt_path)
        prompt_layout.addWidget(self.browse_prompt)

        layout.addLayout(prompt_layout)

        # ---------------- Output Folder ----------------

        output_layout = QHBoxLayout()

        output_label = QLabel("Output Folder:")

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Select Output Folder...")

        self.browse_output = QPushButton("Browse")
        self.browse_output.clicked.connect(self.select_output_folder)

        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.browse_output)

        layout.addLayout(output_layout)

        # ---------------- Buttons ----------------

        button_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶ Start")
        self.pause_btn = QPushButton("⏸ Pause")
        self.stop_btn = QPushButton("⏹ Stop")

        self.start_btn.clicked.connect(self.start_generation)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.stop_btn)

        layout.addLayout(button_layout)

        # ---------------- Progress ----------------

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # ---------------- Log ----------------

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText("Generation log will appear here...")
        layout.addWidget(self.log_box)

        # Logger
        self.logger = Logger(self.log_box)

    # =====================================================
    # Browse Prompt File
    # =====================================================

    def select_prompt_file(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Prompt File",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )

        if file_name:
            self.prompt_path.setText(file_name)
            self.logger.write(f"Prompt File Selected:\n{file_name}")

    # =====================================================
    # Browse Output Folder
    # =====================================================

    def select_output_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )

        if folder:
            self.output_path.setText(folder)
            self.logger.write(f"Output Folder Selected:\n{folder}")

    # =====================================================
    # Start Button
    # =====================================================

    def start_generation(self):

        self.logger.write("====================================")
        self.logger.write("Generation Started...")
        self.logger.write("Ready for next step.")
        self.progress.setValue(5)