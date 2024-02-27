from setuptools import setup, find_packages

setup(
    name='fastmarkup',
    version='0.1',
    packages=find_packages(),
    description='A function-based HTML templating library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Paulo Souza',
    author_email='paulo.roque@hey.com',
    url='https://github.com/pauloevpr/fastmarkup',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
