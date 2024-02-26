from setuptools import setup, find_packages

setup(
    name='RiemannianGeometry',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'sympy',
        'numpy',
        'scipy'
    ],
    author='Simon Wittum',
    author_email='simonwittum@gmx.de',
    description='A package for handling Riemannian manifolds',
    url='https://github.com/swittum/Geometry',
    license='MIT'
)
