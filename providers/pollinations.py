import time
import requests
import urllib.parse


class Pollinations:

    BASE_URL = "https://image.pollinations.ai/prompt/"

    def generate_url(self, prompt):

        prompt = urllib.parse.quote(prompt)

        return f"{self.BASE_URL}{prompt}"

    def download_image(self, prompt, save_path):

        url = self.generate_url(prompt)

        headers = {
            "User-Agent": "Sabbir-AI-Studio/1.0"
        }

        for attempt in range(3):

            try:

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=120
                )

                if response.status_code == 200:

                    with open(save_path, "wb") as file:
                        file.write(response.content)

                    return True

            except requests.RequestException:
                pass

            time.sleep(2)

        return False