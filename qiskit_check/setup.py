from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='qiskit_check',
    version='1.1.1',
    license='MIT',
    author="Marek Grzesiuk",
    packages=['qiskit_check'],
    url='https://github.com/mgrzesiuk/qiskit_check',
    keywords='property-based-testing qiskit quantum-computing',
    install_requires=[
          'qiskit>=0.34.2',
      ],
    description="tool for property based testing in qiskit",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
