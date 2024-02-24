from setuptools import setup, find_packages

VERSION='0.0.3'
DESCRIPTION='working with opencv can be quite a hussel, a lot of boiler code, nested functions for specific use cases, etc, this package is designed to make it easier to work with opencv while focusing on the main task'

setup(
    name='opencv.wrap',
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst').read(),
    url='https://github.com/rishi23root/opencv.util',
    author='rishi23root',
    author_email='rishi23root@gmail.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    ],  
    packages=find_packages(),
    install_requires=['absl-py>=2.1.0', 'attrs>=23.2.0', 'cffi>=1.16.0', 'contourpy>=1.2.0', 'cycler>=0.12.1', 'flatbuffers>=23.5.26', 'fonttools>=4.49.0', 'jax>=0.4.24', 'kiwisolver>=1.4.5', 'matplotlib>=3.8.3', 'mediapipe>=0.10.10', 'ml-dtypes>=0.3.2', 'numpy>=1.26.4', 'opencv-contrib-python>=4.9.0.80', 'opencv-python>=4.9.0.80', 'opt-einsum>=3.3.0', 'packaging>=23.2', 'pillow>=10.2.0', 'protobuf>=3.20.3', 'pycparser>=2.21', 'pyparsing>=3.1.1', 'python-dateutil>=2.8.2', 'scipy>=1.12.0', 'six>=1.16.0', 'sounddevice>=0.4.6'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['pyresparser=pyresparser.command_line:main'],
    }
)
# setup(
#     name='pyresparser',
#     version='1.0.6',
#     description='A simple resume parser used for extracting information from resumes',
#     long_description=open('README.rst').read(),
#     url='https://github.com/OmkarPathak/pyresparser',
#     author='Omkar Pathak',
#     author_email='omkarpathak27@gmail.com',
#     license='GPL-3.0',
#     include_package_data=True,
#     classifiers=[
#         'Intended Audience :: Developers',
#         'Topic :: Software Development :: Libraries',
#         'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.7',
#     ],
#     packages=find_packages(),
#     install_requires=[
#         'attrs>=19.1.0',
#         'blis>=0.2.4',
#         'certifi>=2019.6.16',
#         'chardet>=3.0.4',
#         'cymem>=2.0.2',
#         'docx2txt>=0.7',
#         'idna>=2.8',
#         'jsonschema>=3.0.1',
#         'nltk>=3.4.3',
#         'numpy>=1.16.4',
#         'pandas>=0.24.2',
#         'pdfminer.six>=20181108',
#         'preshed>=2.0.1',
#         'pycryptodome>=3.8.2',
#         'pyrsistent>=0.15.2',
#         'python-dateutil>=2.8.0',
#         'pytz>=2019.1',
#         'requests>=2.22.0',
#         'six>=1.12.0',
#         'sortedcontainers>=2.1.0',
#         'spacy>=2.1.4',
#         'srsly>=0.0.7',
#         'thinc>=7.0.4',
#         'tqdm>=4.32.2',
#         'urllib3>=1.25.3',
#         'wasabi>=0.2.2'
#     ],
#     zip_safe=False,
#     entry_points = {
#         'console_scripts': ['pyresparser=pyresparser.command_line:main'],
#     }
# )