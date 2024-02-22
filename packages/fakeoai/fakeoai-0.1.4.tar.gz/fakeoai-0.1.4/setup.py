from setuptools import setup, find_packages

from fakeoai import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fakeoai',
    version=__version__,
    python_requires='>=3.7',
    author='baobao',
    author_email='yuanbao@fakeopenai.cn',
    keywords='OpenAI ChatGPT',
    description='A Package for local deployment of ChatGPT.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/FakeOpenAI/FakeOpenAI',
    packages=find_packages('fakeoai'),
    include_package_data=True
)
