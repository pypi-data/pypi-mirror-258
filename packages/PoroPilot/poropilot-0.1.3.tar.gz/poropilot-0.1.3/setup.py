from setuptools import setup

# Read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='poropilot',
    version='0.1.3',
    description='Interface for Riot API',
    url='https://github.com/anuiit/PoroPilot',
    author='anui',
    author_email='',
    keywords=['Riot', 'API', 'wrapper', 'Poro', 'Pilot', 'League of Legends', 'LoL', 'game', 'gaming', 'esports', 'riotgames', 'riot-api', 'riot-api-wrapper', 'riot-api-python', 'riot-api'],
    license='MIT',
    packages=['PoroPilot', 'PoroPilot.Endpoints'],
    install_requires=['requests', 'requests-cache'],
    long_description=long_description,
    long_description_content_type='text/markdown',
)