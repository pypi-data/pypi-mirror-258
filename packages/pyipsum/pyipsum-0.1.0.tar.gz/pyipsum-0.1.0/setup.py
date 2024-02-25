from setuptools import setup, find_packages
setup(
    name='pyipsum',
    version='0.1.0',
    author='Tal Zarfati',
    author_email='talzarfati@gmail.com',
    description='Python package sample',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)