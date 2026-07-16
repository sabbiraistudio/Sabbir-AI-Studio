from PySide6.QtCore import QObject, Signal


class ImageWorker(QObject):

    log = Signal(str)
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, csv_reader, pollinations, csv_file, output_folder):
        super().__init__()

        self.csv_reader = csv_reader
        self.pollinations = pollinations
        self.csv_file = csv_file
        self.output_folder = output_folder

        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        import os

        items = self.csv_reader.read_prompts(self.csv_file)

        total = len(items)
        success = 0
        failed = 0

        for index, item in enumerate(items, start=1):

            if self._stop:
                self.log.emit("⛔ Generation Stopped.")
                break

            filename = item["filename"] + ".png"
            save_path = os.path.join(self.output_folder, filename)

            self.log.emit(f"[{index}/{total}] Generating {filename}")

            ok = self.pollinations.download_image(
                item["prompt"],
                save_path
            )

            if ok:
                success += 1
                self.log.emit(f"✅ Saved: {filename}")
            else:
                failed += 1
                self.log.emit(f"❌ Failed: {filename}")

            percent = int((index / total) * 100)
            self.progress.emit(percent)

        self.log.emit("")
        self.log.emit("====================================")
        self.log.emit("Generation Completed")
        self.log.emit(f"Success : {success}")
        self.log.emit(f"Failed  : {failed}")

        self.finished.emit()