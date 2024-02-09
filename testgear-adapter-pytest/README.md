# Test Gear TMS adapter for Pytest

![Test Gear](https://raw.githubusercontent.com/testgear-tms/adapters-python/master/images/banner.png)

[![Release
Status](https://img.shields.io/pypi/v/testgear-adapter-pytest?style=plastic)](https://pypi.python.org/pypi/testgear-adapter-pytest)
[![Downloads](https://img.shields.io/pypi/dm/testgear-adapter-pytest?style=plastic)](https://pypi.python.org/pypi/testgear-adapter-pytest)
[![GitHub contributors](https://img.shields.io/github/contributors/testgear-tms/adapters-python?style=plastic)](https://github.com/testgear-tms/adapters-python)

## Getting Started

### Installation

```
pip install testgear-adapter-pytest
```

## Usage

### Configuration

| Description                                                                                                                                                                                                                                                                                                                                                                            | Property                   | Environment variable              | CLI argument                  |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|-----------------------------------|-------------------------------|
| Location of the TMS instance                                                                                                                                                                                                                                                                                                                                                           | url                        | TMS_URL                           | tmsUrl                        |
| API secret key [How to getting API secret key?](https://github.com/testgear-tms/.github/tree/main/configuration#privatetoken)                                                                                                                                                                                                                                                          | privateToken               | TMS_PRIVATE_TOKEN                 | tmsPrivateToken               |
| ID of project in TMS instance [How to getting project ID?](https://github.com/testgear-tms/.github/tree/main/configuration#projectid)                                                                                                                                                                                                                                                  | projectId                  | TMS_PROJECT_ID                    | tmsProjectId                  |
| ID of configuration in TMS instance [How to getting configuration ID?](https://github.com/testgear-tms/.github/tree/main/configuration#configurationid)                                                                                                                                                                                                                                | configurationId            | TMS_CONFIGURATION_ID              | tmsConfigurationId            |
| ID of the created test run in TMS instance.<br/>It's necessary for **adapterMode** 0 or 1                                                                                                                                                                                                                                                                                              | testRunId                  | TMS_TEST_RUN_ID                   | tmsTestRunId                  |
| Parameter for specifying the name of test run in TMS instance (**It's optional**). If it is not provided, it is created automatically                                                                                                                                                                                                                                                  | testRunName                | TMS_TEST_RUN_NAME                 | tmsTestRunName                |
| Adapter mode. Default value - 0. The adapter supports following modes:<br/>0 - in this mode, the adapter filters tests by test run ID and configuration ID, and sends the results to the test run<br/>1 - in this mode, the adapter sends all results to the test run without filtering<br/>2 - in this mode, the adapter creates a new test run and sends results to the new test run | adapterMode                | TMS_ADAPTER_MODE                  | tmsAdapterMode                |
| It enables/disables certificate validation (**It's optional**). Default value - true                                                                                                                                                                                                                                                                                                   | certValidation             | TMS_CERT_VALIDATION               | tmsCertValidation             |
| Mode of automatic creation test cases (**It's optional**). Default value - false. The adapter supports following modes:<br/>true - in this mode, the adapter will create a test case linked to the created autotest (not to the updated autotest)<br/>false - in this mode, the adapter will not create a test case                                                                    | automaticCreationTestCases | TMS_AUTOMATIC_CREATION_TEST_CASES | tmsAutomaticCreationTestCases |
| Url of proxy server (**It's optional**)                                                                                                                                                                                                                                                                                                                                                | tmsProxy                   | TMS_PROXY                         | tmsProxy                      |
| Name of the configuration file If it is not provided, it is used default file name (**It's optional**)                                                                                                                                                                                                                                                                                 | -                          | TMS_CONFIG_FILE                   | tmsConfigFile                 |

#### File

Create **connection_config.ini** file in the root directory of the project:
```
[testgear]
URL = URL
privateToken = USER_PRIVATE_TOKEN
projectId = PROJECT_ID
configurationId = CONFIGURATION_ID
testRunId = TEST_RUN_ID
testRunName = TEST_RUN_NAME
adapterMode = ADAPTER_MODE
certValidation = CERT_VALIDATION
automaticCreationTestCases = AUTOMATIC_CREATION_TEST_CASES

# This section are optional. It enables debug mode.
[debug]
tmsProxy = TMS_PROXY
```

#### Examples

Launch with a connection_config.ini file in the root directory of the project:

```
$ pytest --testgear
```

Launch with command-line parameters:

```
$ pytest --testgear --tmsUrl=URL --tmsPrivateToken=USER_PRIVATE_TOKEN --tmsProjectId=PROJECT_ID --tmsConfigurationId=CONFIGURATION_ID --tmsTestRunId=TEST_RUN_ID --tmsTestRunName=TEST_RUN_NAME --tmsAdapterMode=ADAPTER_MODE --tmsProxy='{"http":"http://localhost:8888","https":"http://localhost:8888"}' --tmsCertValidation=CERT_VALIDATION --tmsAutomaticCreationTestCases=AUTOMATIC_CREATION_TEST_CASES
```

If you want to enable debug mode then
see [How to enable debug logging?](https://github.com/testgear-tms/adapters-python/tree/main/testgear-python-commons)

### Decorators

Decorators can be used to specify information about autotest.

Description of decorators:

- `testgear.workItemIds` - a method that links autotests with manual tests. Receives the array of manual tests' IDs
- `testgear.displayName` - internal autotest name (used in Test Gear)
- `testgear.externalId` - unique internal autotest ID (used in Test Gear)
- `testgear.title` - autotest name specified in the autotest card. If not specified, the name from the displayName method is used
- `testgear.description` - autotest description specified in the autotest card
- `testgear.labels` - tags listed in the autotest card
- `testgear.link` - links listed in the autotest card
- `testgear.step` - the designation of the step called in the body of the test or other step
- `testgear.nameSpace` - directory in the TMS system (default - file's name of test)
- `testgear.className` - subdirectory in the TMS system (default - class's name of test)

All decorators support the use of parameterization attributes

Description of methods:

- `testgear.addLinks` - links in the autotest result
- `testgear.addAttachments` - uploading files in the autotest result
- `testgear.addMessage` - information about autotest in the autotest result
- `testgear.step` - usage in the "with" construct to designation a step in the body of the test

### Examples

#### Simple test

```py
import pytest
import testgear


# Test with a minimal set of decorators
@testgear.externalId('Simple_autotest2')
def test_2():
    """Simple autotest 2"""
    assert oneStep()
    assert twoStep()


@testgear.step
def oneStep():
    assert oneOneStep()
    assert oneTwoStep()
    return True


@testgear.step
def twoStep():
    return True


@testgear.step('step 1.1', 'description')
def oneOneStep():
    return True


@testgear.step('step 2')
def oneTwoStep():
    return True


@testgear.externalId('Simple_test_skip')
@testgear.displayName('Simple test skip')
@testgear.links(url='https://dumps.example.com/module/JCP-777')
@testgear.links(url='https://dumps.example.com/module/JCP-777',
              title='JCP-777',
              type=testgear.LinkType.RELATED,
              description='Description of JCP-777')
@pytest.mark.skipif(True, reason='Because i can')
def test_skip():
    assert True
```

#### Parameterized test

```py
# Parameterized test with a full set of decorators
from os.path import join, dirname

import pytest
import testgear


@testgear.workItemIds(627)
@testgear.displayName('Simple autotest 1 - {name}')
@testgear.externalId('Simple_autotest1_{name}')
@testgear.title('Authorization')
@testgear.description('E2E_autotest')
@testgear.labels('{labels}')
@testgear.links(links=[
    {'url': '{url}', 'type': '{link_type}', 'title': '{link_title}', 'description': '{link_desc}'},
    {'url': '{url}', 'type': '{link_type}', 'title': '{link_title}', 'description': '{link_desc}'}
])
@pytest.mark.parametrize('name, labels, url, link_type, link_title, link_desc', [
    ('param 1', ['E2E', 'test'], 'https://dumps.example.com/module/JCP-777', testgear.LinkType.DEFECT, 'JCP-777',
     'Desc of JCP-777'),
    ('param 2', (), 'https://dumps.example.com/module/docs', testgear.LinkType.RELATED, 'Documentation',
     'Desc of JCP-777'),
    ('param 3', ('E2E', 'test'), 'https://dumps.example.com/module/projects', testgear.LinkType.REQUIREMENT, 'Projects',
     'Desc of Projects'),
    ('param 4', {'E2E', 'test'}, 'https://dumps.example.com/module/', testgear.LinkType.BLOCKED_BY, '', ''),
    ('param 5', 'test', 'https://dumps.example.com/module/repository', testgear.LinkType.REPOSITORY, 'Repository',
     'Desc of Repository')
])
def test_1(name, labels, url, link_type, link_title, link_desc):
    testgear.addLinks(url='https://dumps.example.com/module/some_module_dump', title='component_dump.dmp',
                    type=testgear.LinkType.RELATED, description='Description')
    testgear.addLinks(url='https://dumps.example.com/module/some_module_dump')
    testgear.addLinks(links=[
        {'url': 'https://dumps.example.com/module/some_module_dump', 'type': testgear.LinkType.BLOCKED_BY,
         'title': 'component_dump.dmp', 'description': 'Description'},
        {'url': 'https://dumps.example.com/module/some_module_dump', 'type': testgear.LinkType.DEFECT},
        {'url': 'https://dumps.example.com/module/some_module_dump', 'type': testgear.LinkType.ISSUE,
         'title': 'component_dump.dmp'},
        {'url': 'https://dumps.example.com/module/some_module_dump', 'type': testgear.LinkType.REQUIREMENT,
         'title': 'component_dump.dmp', 'description': 'Description'},
        {'url': 'https://dumps.example.com/module/some_module_dump', 'type': testgear.LinkType.REPOSITORY,
         'description': 'Description'},
        {'url': 'https://dumps.example.com/module/some_module_dump'}
    ])
    with testgear.step('Log in the system', 'system authentication'):
        with testgear.step('Enter the login', 'login was entered'):
            with testgear.step('Enter the password', 'password was entered'):
                assert True
        with testgear.step('Create a project', 'the project was created'):
            with testgear.step('Enter the project', 'the contents of the project are displayed'):
                assert True
            with testgear.step('Create a test case', 'test case was created'):
                assert True
    with testgear.step('Attachments'):
        testgear.addAttachments(
            join(dirname(__file__), 'docs/text_file.txt'),
            join(dirname(__file__), 'pictures/picture.jpg'),
            join(dirname(__file__), 'docs/document.docx')
        )
        testgear.addAttachments(
            join(dirname(__file__), 'docs/document.doc'),
            join(dirname(__file__), 'docs/logs.log')
        )
        assert True
```

# Contributing

You can help to develop the project. Any contributions are **greatly appreciated**.

* If you have suggestions for adding or removing projects, feel free
  to [open an issue](https://github.com/testgear-tms/adapters-python/issues/new) to discuss it, or directly create a pull
  request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through
  the [Code Of Conduct](https://github.com/testgear-tms/adapters-python/blob/master/CODE_OF_CONDUCT.md) before posting
  your first idea as well.

# License

Distributed under the Apache-2.0 License.
See [LICENSE](https://github.com/testgear-tms/adapters-python/blob/master/LICENSE.md) for more information.

