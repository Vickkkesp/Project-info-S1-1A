import os
from PIL import Image

def convert_to_jpg(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith((".png", ".webp", ".avif")):
                path = os.path.join(root, file)
                img = Image.open(path).convert("RGB")
                new_name = os.path.splitext(file)[0] + ".jpg"
                new_path = os.path.join(root, new_name)
                img.save(new_path, "JPEG")
                print(f"Converted: {path} -> {new_path}")

def remove_non_jpg_images(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if not file.lower().endswith(".jpg"):
                path = os.path.join(root, file)
                try:
                    os.remove(path)
                    print(f"Deleted: {path}")
                except Exception as e:
                    print(f"Error deleting {path}: {e}")

if __name__ == "__main__":
    base_folders = [
        "static/Images",
        "static/Images/produits"
    ]
    for folder in base_folders:
        convert_to_jpg(folder)
    for folder in base_folders:
        remove_non_jpg_images(folder)
