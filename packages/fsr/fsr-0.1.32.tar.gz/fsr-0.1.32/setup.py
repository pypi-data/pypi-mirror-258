from setuptools import setup, find_packages

setup(
    name='fsr',
    version='0.1.32',
    author='Roman Pluzhnikov',
    author_email='pluzhnikov137@gmail.com',
    description='CLI tool for generating and serving test reports',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rpluzhnikov/fsr',
    package_data={
        'reporter': ['report_web/*', 'report_web/*/*'], 
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'fsr=reporter.main:main', 
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
