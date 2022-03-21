from setuptools import setup
import pathlib

readme = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name='my-quickbase',
    version='0.2.0',
    url='https://github.com/samw1989/my-quickbase',
    packages=['my_quickbase'],
    license='MIT',
    author='Sam Westrop',
    author_email='westrop@meforum.org',
    description='A lightweight tool for interacting with Quickbase\'s RESTful API',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=['pytest', 'requests', 'python-decouple']
)
