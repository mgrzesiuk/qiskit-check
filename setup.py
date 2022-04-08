from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent


setup(
    name='qiskit_check',
    version='1.1.1',
    license='MIT',
    author="Marek Grzesiuk",
    packages=find_packages(include=['qiskit_check', 'qiskit_check.*']),
    url='https://github.com/mgrzesiuk/qiskit_check',
    keywords='property-based-testing qiskit quantum-computing',
    install_requires=[
          'qiskit==0.34.2',
          'numpy==1.21.2',
          'scipy==1.7.2',
          'pyyaml==6.0',
          'colorama==0.4.4',
          'qiskit-utils==1.1.5',
    ],
    description="tool for property based testing in qiskit",
    long_description="library for property based testing of quantum programs written in qiskit",
    long_description_content_type='text/markdown'
)
