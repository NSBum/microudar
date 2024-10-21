from setuptools import setup, find_packages

setup(
    name='microudar',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'zmq',
        'stressrnn @ git+https://github.com/Desklop/StressRNN'
    ],
    entry_points={
        'console_scripts': [
            'start-microudar-service = microudar.service:start_service',
        ],
    },
    description='A microservice for applying Russian syllabic stress marks based on StressRNN',
    author='Alan K. Duncan',
    author_email='microudar+alan@fastmail.com',
    url='https://github.com/NSBum/microudar',
)

from setuptools import setup, find_packages
