from setuptools import setup, find_packages

setup(
    name='PyFolioC',
    version='0.1',
    packages=find_packages(),
    author='Naïl Khelifa',
    author_email='nail.khelifa@ensae.fr',
    description='Portfolio Optimization Package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NailKhelifa/PyFolioC',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy>=1.24.3', 
        'pandas>=2.0.3', 
        'scipy>=1.11.1', 
        'matplotlib>=3.7.2',
        'seaborn>=0.12.2', 
        'PyPortfolioOpt>=1.5.4'
    ],
)