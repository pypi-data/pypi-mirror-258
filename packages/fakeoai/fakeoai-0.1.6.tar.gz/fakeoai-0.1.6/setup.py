from setuptools import setup

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
    packages=['fakeoai'],
    package_dir={'fakeoai': 'fakeoai'},
    package_data={"fakeoai": ["flask/**"]},
    include_package_data=True,
    install_requires=[
        "flask",
        "python-dotenv",
        "requests"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Environment :: Web Environment',

        'Framework :: Flask',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
