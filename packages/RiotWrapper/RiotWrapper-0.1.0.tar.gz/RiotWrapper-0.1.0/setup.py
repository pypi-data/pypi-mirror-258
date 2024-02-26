from setuptools import setup

setup(
    name='RiotWrapper',
    version='0.1.0',
    description='Interface for Riot API',
    url='https://github.com/anuiit/RiotWrapper',
    author='anui',
    author_email='',
    keywords=['Riot', 'API', 'wrapper'],
    license='BSD 2-clause',
    packages=['Wrapper'],
    install_requires=['requests', 'requests-cache'],
    python_requires='>=3.6',
    long_description="Your detailed description goes here.",

)