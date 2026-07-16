import csv


class CSVReader:

    def read_prompts(self, file_path):

        prompts = []

        with open(file_path, "r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                prompt = row.get("Prompt", "").strip()

                if prompt:
                    prompts.append(prompt)

        return prompts