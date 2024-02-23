from setuptools import setup, find_packages

setup(
    name='Picklejuice',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'argparse',  # This is part of the standard library, no need to include it
    ],
    entry_points={
        'console_scripts': [
            'picklejuice=picklejuice.main:main',
        ],
    },
    author='Kyle Reynolds',
    author_email='kylereynoldsdev@gmail.com',
    description='Cli tool for quickly translating JSON and YAML config files to Pkl.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KDreynolds/vinegar',
)