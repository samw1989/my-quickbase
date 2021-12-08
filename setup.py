from setuptools import setup

setup(
    name='my-quickbase',
    version='0.1.1',
    url='https://github.com/samw1989/my-quickbase',
    packages=['my_quickbase'],
    license='MIT',
    author='Sam Westrop',
    author_email='westrop@meforum.org',
    description='A lightweight tool for interacting with Quickbase\'s RESTful API',
    include_package_data=True,
    install_requires=['pytest', 'requests', 'python-decouple']
)
