from setuptools import setup, find_packages

setup(
    name="afish-task-tracker",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'tkinter',
    ],
    author="AFISH",
    description="A modern task tracking application",
    python_requires='>=3.6',
) 