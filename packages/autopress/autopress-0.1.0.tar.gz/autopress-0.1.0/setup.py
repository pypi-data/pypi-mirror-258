from setuptools import setup, find_packages
__version__ = "0.1.0"

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="autopress",
    version=__version__,
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Edward Laurence",
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'autopress=autopress.cli:main',
        ],
    }
)