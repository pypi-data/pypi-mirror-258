from setuptools import setup, find_packages

setup(
    name='coordinate_conversion',
    version='0.1.2',
    packages=find_packages(),
    description='A Python package for converting coordinates between Cartesian, spherical, and cylindrical systems.',
    author='xwebname',
    author_email='xwebname@protonmail.com',
    license='MIT',
    install_requires=['numpy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
