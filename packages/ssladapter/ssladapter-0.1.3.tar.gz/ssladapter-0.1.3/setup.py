from setuptools import setup, find_packages

setup(
    name='ssladapter',
    version='0.1.3',
    packages=find_packages(),
    install_requires=['requests==2.27.1'],
    python_requires='>=3.6',
    author='Lorenzo Fabro',
    author_email='lorenzofabro1997@gmail.com',
    description='SSL Adapter for requests library',
    url='https://github.com/lorenzofabro/ssladapter',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
)
