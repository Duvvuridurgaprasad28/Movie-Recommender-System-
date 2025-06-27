# setup.py placeholder
from setuptools import setup, find_packages

def read_requirements():
    """Reads and filters requirements.txt"""
    with open("requirements.txt", "r") as file:
        requirements = [line.strip() for line in file.readlines() if not line.startswith("-e")]
    return requirements

setup(
    name="movie_recommender_mlops",
    version="1.0",
    author="Durga",
    description="An MLOps-based movie recommender system",
    packages=find_packages(),
    install_requires=read_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)