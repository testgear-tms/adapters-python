from setuptools import setup, find_packages

setup(
    name='testgear-python-commons',
    version='2.0.9',
    description='Python commons for Test Gear',
    url='https://github.com/testgear-tms/adapters-python/',
    author='Integration team',
    author_email='integrations@test-gear.io',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    py_modules=['testgear', 'testgear_python_commons'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['pluggy', 'testgear-api-client==2.0.2']
)
