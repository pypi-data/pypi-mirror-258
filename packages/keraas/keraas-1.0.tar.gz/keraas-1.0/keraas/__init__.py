# keraas/__init__.py

import os

# Get the directory path where the .txt files are located
txt_dir_path = os.path.dirname(os.path.realpath(__file__))

# Define functions to print the code from .txt files
def cgan():
    with open(os.path.join(txt_dir_path, 'cgan.txt'), 'r') as file:
        code = file.read()
        print("Code in cgan.txt:")
        print(code)

def mod1():
    with open(os.path.join(txt_dir_path, 'mod1.txt'), 'r') as file:
        code = file.read()
        print("Code in mod1.txt:")
        print(code)

def diffusion():
    with open(os.path.join(txt_dir_path, 'diffusion.txt'), 'r') as file:
        code = file.read()
        print("Code in diffusion.txt:")
        print(code)

def rcnn():
    with open(os.path.join(txt_dir_path, 'rcnn.txt'), 'r') as file:
        code = file.read()
        print("Code in rcnn.txt:")
        print(code)

def face():
    with open(os.path.join(txt_dir_path, 'face.txt'), 'r') as file:
        code = file.read()
        print("Code in face.txt:")
        print(code)

def image():
    with open(os.path.join(txt_dir_path, 'image.txt'), 'r') as file:
        code = file.read()
        print("Code in image.txt:")
        print(code)

def stable():
    with open(os.path.join(txt_dir_path, 'stable.txt'), 'r') as file:
        code = file.read()
        print("Code in stable.txt:")
        print(code)

def vae():
    with open(os.path.join(txt_dir_path, 'vae.txt'), 'r') as file:
        code = file.read()
        print("Code in vae.txt:")
        print(code)

def yoloc():
    with open(os.path.join(txt_dir_path, 'yoloc.txt'), 'r') as file:
        code = file.read()
        print("Code in yoloc.txt:")
        print(code)

def yolo():
    with open(os.path.join(txt_dir_path, 'yolo.txt'), 'r') as file:
        code = file.read()
        print("Code in yolo.txt:")
        print(code)
