from setuptools import setup, find_packages

setup(
    name='keraas',
    version='1.9',
    packages=find_packages(),
    package_data={
        'keraas': ['*.txt']
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
     long_description_content_type='text/markdown',
    url='http://example.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='keraas',
)
