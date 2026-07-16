import os

from providers.pollinations import Pollinations


def main():

    provider = Pollinations()

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    save_path = os.path.join(output_dir, "test_image.png")

    prompt = (
        "Minimalist black silhouette of a lion, "
        "clean vector style, white background"
    )

    print("Generating image...")

    success = provider.download_image(prompt, save_path)

    if success:
        print("SUCCESS!")
        print(f"Saved to: {save_path}")
    else:
        print("FAILED!")


if __name__ == "__main__":
    main()