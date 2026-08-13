import os
import shutil

# path eg: ./public
def copy_content_static_to_public_built_in(src: str, dest: str):
    # create public directory if it doesnt exist, delete and recreate if it exists
    try:
        dest_exists = os.path.exists(dest)
        if dest_exists:
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    except:
        raise Exception(f"copying content from {src} to {dest} failed")

def copy_content_static_to_public_recursive(src: str, dest: str):
    print(f"copying content from {src} to {dest}")
    try:
        dest_exists = os.path.exists(dest)
        if dest_exists:
            shutil.rmtree(dest)
            os.mkdir(dest)
        else:
            os.mkdir(dest)
        static_contents = os.listdir(src)
        for file_item in static_contents:
            src_item_path = os.path.join(src, file_item)
            dest_item_path = os.path.join(dest, file_item)
            print(src_item_path)
            print(dest_item_path)
            if os.path.isfile(src_item_path):
                shutil.copy(src_item_path, dest_item_path)
            else:
                copy_content_static_to_public_recursive(src_item_path, dest_item_path)
    except:
       raise Exception(f"copying content from {src} to {dest} failed") 