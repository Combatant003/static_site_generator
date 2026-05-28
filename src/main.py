import os
import sys
import shutil
from generate_page import generate_page


def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            copy_static(src_path, dst_path)


def generate_pages_recursive(content_dir, template_path, dest_dir, basepath="/"):
    for item in os.listdir(content_dir):
        src_path = os.path.join(content_dir, item)
        dst_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_path) and item.endswith(".md"):
            dest_html = dst_path[:-3] + ".html"
            generate_page(src_path, template_path, dest_html, basepath)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
