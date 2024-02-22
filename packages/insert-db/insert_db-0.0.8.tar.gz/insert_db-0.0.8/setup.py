from setuptools import setup, find_packages

setup(
    name = 'insert_db',
    version= '0.0.8',
    description= ' Connect pandas to postgresql database to insert data',
    author= 'jerry',
    author_email='dnl6097@gmail.com',
    url='https://github.com/wisangyun/myfile.git',
    install_requires = ['tqdm','sqlalchemy'],
    packages=find_packages(exclude=[]),
    keywords=['insert_db','database','postgresql','python','pypi'],
    python_requires = '>=3.8',
    package_data={},
    zip_safe = False,
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    include_package_data=True
)