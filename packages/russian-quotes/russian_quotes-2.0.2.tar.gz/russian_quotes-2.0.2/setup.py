from setuptools import setup


def readme():
    """
    Read the contents of README.md file.

    Returns:
        str: The contents of README.md file as a string.
    """
    with open('README.md', encoding="utf-8") as file:
        _readme = file.read()

    return _readme


setup(
    name='russian_quotes',
    version='2.0.2',
    author='liner',
    author_email='contact.liner999@gmail.com',
    description='Quotes of famous people in russian',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['russian_quotes'],
    project_urls={
      'GitHub': 'https://github.com/r-liner/russian_quotes/',
      'Bug Tracker': 'https://github.com/r-liner/russian_quotes/issues'
    },
    package_data={'epic_free_games': ["VERSION"]},
    include_package_data=True,
    install_requires=['aiohttp', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
