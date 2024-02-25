from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='p2k',  # required
    version='2024.2.24',
    description='p2k: utilities for the Aggregated Common Era Paleoclimate Database',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Feng Zhu, Michael N. Evans',
    author_email='fengzhu@ucar.edu, mnevans@umd.edu',
    url='https://github.com/fzhu2e/p2k',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords='paleoclimate database, Common Era',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'colorama',
        'seaborn',
        'pandas',
        'scipy',
        'tqdm',
        'xarray',
        'netCDF4',
        'nc-time-axis',
        'dask',
        'plotly',
        'pylipd',
    ],
)
