import setuptools

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setuptools.setup(
    name='grigode_env',
    version='1.0.1',
    author='Angel Chávez',
    author_email='infoangelchavez@gmail.com',
    description="grigode_env reads key-value pairs from a '.env' file and "
                "parses them into various data types.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/angelchavez19/grigode_env',
    project_urls={
        'Bug Tracker': 'https://github.com/angelchavez19/grigode_env/issues'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.10'
)
