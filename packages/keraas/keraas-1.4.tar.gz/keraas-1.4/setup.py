from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='keraas',
    version='1.4',
    author='Your Name',
    author_email='your@email.com',
    description='Description of your package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/keraas',
    packages=find_packages(),
    package_data={'keraas': ['*.txt']},
    entry_points={
        'console_scripts': [
            'cgan = keraas:cgan',
            'mod1 = keraas:mod1',
            'diffusion = keraas:diffusion',
            'rcnn = keraas:rcnn',
            'face = keraas:face',
            'image = keraas:image',
            'stable = keraas:stable',
            'vae = keraas:vae',
            'yoloc = keraas:yoloc',
            'yolo = keraas:yolo',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
