from setuptools import setup, find_packages

setup(
    name='flaskk',
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    description='A simple test package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_test',
    install_requires=[
        # Any dependencies, e.g., 'requests >= 2.19.1'
    ],
)
