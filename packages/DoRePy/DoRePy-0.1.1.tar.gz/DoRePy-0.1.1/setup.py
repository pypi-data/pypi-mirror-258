from setuptools import setup, find_packages

setup(
    name="DoRePy",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
           'dorepy=DoRePy.dorepy:main',
        ],
    },
    python_requires='>=3.6',
    description="A tool for downloading files with filenames matching user-specified regex patterns which are linked to on a user-provided URL",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Cillian Scott",
    author_email="scottci@tcd.ie",
    url="https://github.com/CillySu/DoRePy",
)
