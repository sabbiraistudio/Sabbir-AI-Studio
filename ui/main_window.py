import os

from PySide6.QtCore import QThread

from workers.image_worker import ImageWorker

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
from core.csv_reader import CSVReader
from providers.pollinations import Pollinations


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

        self.csv_reader = CSVReader()
        self.pollinations = Pollinations()

        self.thread = None
        self.worker = None

        self.stop_btn.clicked.connect(self.stop_generation)

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

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

    self.logger.clear()

    self.logger.write("====================================")
    self.logger.write("Generation Started...\n")

    csv_file = self.prompt_path.text()
    output_folder = self.output_path.text()

    if not output_folder:
        self.logger.write("No Output Folder Selected!")
        return

    if not csv_file:
        self.logger.write("No Prompt File Selected!")
        return

    self.progress.setValue(0)

    self.thread = QThread()

    self.worker = ImageWorker(
        self.csv_reader,
        self.pollinations,
        csv_file,
        output_folder
    )

        self.worker.moveToThread(self.thread)

    self.thread.started.connect(self.worker.run)

    self.worker.log.connect(self.logger.write)
    self.worker.progress.connect(self.progress.setValue)

    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)

    self.worker.finished.connect(self.generation_finished)

    self.start_btn.setEnabled(False)
    self.stop_btn.setEnabled(True)

    self.thread.start()

        for index, item in enumerate(items, start=1):

            filename = item["filename"] + ".png"
            save_path = os.path.join(output_folder, filename)

            self.logger.write(
                f"[{index}/{total}] Generating {filename}"
            )

            success = self.pollinations.download_image(
                item["prompt"],
                save_path
            )

            if success:
                self.logger.write(f"✅ Saved: {filename}")
            else:
                self.logger.write(f"❌ Failed: {filename}")

            progress = int((index / total) * 100)
            self.progress.setValue(progress)

        self.logger.write("\n🎉 All images generated successfully.")

    def stop_generation(self):

        if self.worker:
            self.worker.stop()

            def generation_finished(self):

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        self.thread = None
        self.worker = None