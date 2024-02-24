from setuptools import setup, find_packages
import os

# Function to find all text files in the specified directory
def find_data_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.txt'):
                paths.append(os.path.join(path, filename))
    return paths

# List all package data files (including .txt files)
package_data = find_data_files('keraas/keraas')

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='keraas',
    version='1.0',
    url='https://github.com/yourusername/keraas',
    packages=find_packages(),
    author='Your Name',
    author_email='your@email.com',
    description='Description of your package',
    package_data={'keraas': package_data},
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'cgan = keraas.cgan:main',
            'mod1 = keraas.mod1:main',
            'diffusion = keraas.diffusion:main',
            'rcnn = keraas.rcnn:main',
            'face = keraas.face:main',
            'image = keraas.image:main',
            'stable = keraas.stable:main',
            'vae = keraas.vae:main',
            'yoloc = keraas.yoloc:main',
            'yolo = keraas.yolo:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
