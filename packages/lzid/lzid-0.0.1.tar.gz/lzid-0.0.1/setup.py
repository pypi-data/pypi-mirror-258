import lzid
from pathlib import Path
from setuptools import setup, find_packages

project_base_url = 'https://dev.azure.com/dev-the-office/_git/lzid'

setup(
    name=lzid.__name__,
    packages=find_packages(exclude=('tests', 'tests.*')),
    package_data={lzid.__name__: ['py.typed']},
    version=lzid.__version__,
    description=lzid.__doc__,
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    author='Tomas Maggio',
    author_email='tomas-github@maggio.nz',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    license='MIT License',
    url=project_base_url,
    download_url=project_base_url + 'archive/master.zip',
    python_requires='>=3.7',
    install_requires=Path('requirements.txt').read_text(encoding='utf-8')
)
