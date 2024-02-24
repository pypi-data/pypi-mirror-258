from setuptools import setup,find_packages

setup(
    name="json-clip",
    version="1.0.2",
    author="Chadalawada Siva Bala Krishna Chowdary",
    packages=find_packages(),
    nclude_package_data=True,
    entry_points={
        'console_scripts': [
            'clip = src.main:main'
        ]
    },
    author_email="sivachadalawada1923@gmail.com",
    description="A command-line utility for efficient management of text snippets and keys, designed to simplify the storage, retrieval, and organization of frequently used text and commands",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Siva-0310/clip",
     classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)