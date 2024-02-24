from setuptools import setup

setup(
    name='comfit',
    version='1.2.2',
    packages=['comfit'],
    package_data={'comfit':['core/*','models/*','tools/*']},
    author='Vidar Skogvoll and Jonas Rønning',
    install_requires=['numpy',
                      'scipy',
                      'scikit-image',
                      'matplotlib',
                      'moviepy==1.0.3',
                      'imageio',
                      'vtk',
                      'PyQt5',
                      'mayavi==4.8.1'],
)