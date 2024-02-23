from setuptools import setup, find_packages

setup(
    name='conf-mat',
    version='1.0.1',
    author='khiat Mohammed Abderrezzak',
    author_email='khiat.abderrezzak@gmail.com',
    description='Sophisticate Open Confusion Matrix',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "tabulate>=0.9.0",
        "termcolor>=2.4.0",
        "numpy>=1.26.4",
        "matplotlib>=3.8.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
