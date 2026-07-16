import requests
import urllib.parse


class Pollinations:

    BASE_URL = "https://image.pollinations.ai/prompt/"

    def generate_url(self, prompt):

        prompt = urllib.parse.quote(prompt)

        return f"{self.BASE_URL}{prompt}"

    def download_image(self, prompt, save_path):

        url = self.generate_url(prompt)

        response = requests.get(url, timeout=120)

        if response.status_code == 200:

            with open(save_path, "wb") as file:
                file.write(response.content)

            return True

        return False