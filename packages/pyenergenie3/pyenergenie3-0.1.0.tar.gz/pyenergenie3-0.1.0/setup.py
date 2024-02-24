from setuptools import setup, find_packages

setup(
    name='pyenergenie3',
    version='0.1.0',
    description='Python 3 library for controlling the EnerGenie power strip EG-PMS2-LANSW',
    author='r3turnNull',
    author_email='r3turnNull@protonmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
