from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='embed-builder.pt-br',
    version='0.0.1',
    license='MIT License',
    author='Leticia Sousa',
    long_description=readme,
    author_email='leticialimasousa2007@gmail.com',
    packages=['Embed_Builder'],
    install_requires=['discord.py'])
