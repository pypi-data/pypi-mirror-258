from setuptools import setup, find_packages

setup(
    name="secwebapi",
    version="0.1",
    description="A Python package to interact with the Secwe API",
    author="Samet Azaboglu",
    author_email="sametazaboglu@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
)