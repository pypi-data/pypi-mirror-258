from setuptools import setup, find_packages

setup(
    name='keyword-collector',
    version='0.0.1',
    description='PYPI package to collect keywords',
    author='kkj4980',
    author_email='kkj4980.kim@gmail.com',
    url='https://github.com/KyungjunKim726/keyword_provider',
    install_requires=['selenium', 'asyncio', ],
    packages=find_packages(exclude=[]),
    keywords=['keyword'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)