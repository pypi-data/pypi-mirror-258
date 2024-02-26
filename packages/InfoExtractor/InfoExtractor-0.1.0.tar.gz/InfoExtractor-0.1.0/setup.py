from setuptools import setup, find_packages

setup(
    name='InfoExtractor',
    version='0.1.0',
    author='Alex Jeschor',
    author_email='alx.j.lab@gmail.com',
    description='A Python package for extracting phone numbers, links, and emails from text.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AJeschor/InfoExtractor',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Text Processing :: Linguistic',
    ],
)
