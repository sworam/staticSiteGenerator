import os
import shutil

from page_generator import generate_pages_recursive


def copy_recursively(src: str, dest: str) -> None:
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    objects = os.listdir(src)
    for obj in objects:
        src_path = os.path.join(src, obj)
        dst_path = os.path.join(dest, obj)
        if os.path.isfile(src_path):
            print(f"copying file {obj} from {src} to {dest}")
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            print(f"copying directory {obj} from {src} to {dest}")
            copy_recursively(src_path, dst_path)



def main():
    copy_recursively("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
