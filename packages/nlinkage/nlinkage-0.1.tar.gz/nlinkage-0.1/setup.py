from setuptools import setup, find_packages

setup(
    name='nlinkage',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nlinkage = nlinkage.main:main',
        ],
    },
    author='Ami',
    author_email='idonthavemail@gmail.com',
    description='A package for modifying links in HTML files for GitHub preview.',
    url='https://github.com/yourusername/your_package',
    install_requires=['beautifulsoup4'],  # List any dependencies here
)
