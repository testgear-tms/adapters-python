from setuptools import setup

setup(
    name='testgear-adapter-pytest',
    version='1.0.0',
    description='Pytest adapter for TestGear',

    url='https://pypi.org/project/testgear-adapter-pytest/',
    author='Pavel Butuzov',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    py_modules=['testgear', 'testgear_adapter_pytest'],
    packages=['testgear_adapter_pytest'],
    package_dir={'testgear_adapter_pytest': 'src'},
    install_requires=['pytest', 'pytest-xdist', 'testgear-api-client'],
    entry_points={'pytest11': ['testgear_adapter_pytest = testgear_adapter_pytest.plugin']}
)
