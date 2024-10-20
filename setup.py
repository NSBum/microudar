from setuptools import setup, find_packages

setup(
    name='microudar',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'zmq',
        'stressrnn @ git+https://github.com/Desklop/StressRNN'
    ],
    description='A microservice for applying Russian syllabic stress marks based on StressRNN',
    author='Alan K. Duncan',
    author_email="microudar+alan@fastmail.com',
    url = 'https://github.com/NSBum/microudar',
)
