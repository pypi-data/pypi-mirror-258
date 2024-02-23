from setuptools import setup, find_packages

setup(
    name="secwebapi",
    version="2024.01",
    description="A Python package to interact with the Secwe API",
    url="https://secwe.pythonanywhere.com",
    author="Samet Azaboglu",
    author_email="sametazaboglu@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tldextract",
    ],
)