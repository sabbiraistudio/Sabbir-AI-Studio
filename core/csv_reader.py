import csv


class CSVReader:

    def read_prompts(self, file_path):

        items = []

        with open(file_path, "r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                filename = (
                    row.get("Filename")
                    or row.get("filename")
                    or ""
                ).strip()

                prompt = (
                    row.get("Prompt")
                    or row.get("prompt")
                    or ""
                ).strip()

                if prompt:

                    items.append(
                        {
                            "filename": filename,
                            "prompt": prompt
                        }
                    )

        return items