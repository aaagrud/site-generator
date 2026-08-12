import os
import shutil

# path eg: ./public
def copy_content_static_to_public(src: str, dest: str):
    # create public directory if it doesnt exist, delete and recreate if it exists
    try:
        public_exists = os.path.exists(dest)
        if public_exists:
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    except:
        raise Exception(f"copying content from {src} to {dest} failed")