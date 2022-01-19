# TestGear TMS adapters for Python
![TestGear](https://raw.githubusercontent.com/testgear-tms/adapters-python/main/images/banner.png)

# Pytest

## Getting Started

### Installation
```
pip install testgear-adapter-pytest
```

## Usage

### API client

To use adapter you need to install `testgear-api-client`:
```
pip install testgear-api-client
```

### Configuration

Create `connection_config.ini` file in the root directory of the project:
```
[testgear]
url = https://{DOMAIN} - location of the TestGear instance
privatetoken = it has the form {T2lKd2pLZGI4WHRhaVZUejNl}
    1. go to the https://{DOMAIN}/user-profile profile
    2. copy the API secret key
projectID = it has the form {5236eb3f-7c05-46f9-a609-dc0278896464}
    1. create a project
    2. open DevTools -> network
    3. go to the project https://{DOMAIN}/projects/20/tests
    4. GET-request project, Preview tab, copy id field
configurationID = it has the form {15dbb164-c1aa-4cbf-830c-8c01ae14f4fb}
    1. create a project
    2. open DevTools -> network
    3. go to the project https://{DOMAIN}/projects/20/tests
    4. GET-request configurations, Preview tab, copy id field
testrun_name = {NAME} - optional parameter for specifying the name of test-run in TestGear
```

### Tags

Decorators can be used to specify information about autotest.

Description of decorators (\* - required):
- `testgear.workItemID` - linking an autotest to a test case
- \*`testgear.displayName` - name of the autotest in the TestGear system (can be replaced with documentation strings)
- \*`testgear.externalID` - ID of the autotest within the project in the TestGear System
- `testgear.title` - title in the autotest card
- `testgear.description` - description in the autotest card
- `testgear.labels` - tags in the work item
- `testgear.link` - links in the autotest card
- `testgear.step` - the designation of the step called in the body of the test or other step

All decorators support the use of parameterization attributes

Description of methods:
- `testgear.addLink` - links in the autotest result
- `testgear.step` - usage in the "with" construct to designation a step in the body of the test
- `testgear.attachments` - uploading files in the autotest result
- `testgear.message` - information about autotest in the autotest result

### Examples

#### Decorators
```py
import pytest
import testgear

# Test with a minimal set of decorators
@testgear.externalID('Simple_autotest2')
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

@testgear.externalID('Simple_test_skip')
@testgear.displayName('Simple test skip')
@pytest.mark.skipif(True, reason='Because i can')
def test_skip():
    assert True
```

#### Parameterized test
```py
# Parameterized test with a full set of decorators
@testgear.workItemID(627)
@testgear.displayName('Simple autotest 1 - {name}')
@testgear.externalID('Simple_autotest1_{name}')
@testgear.title('Authorization')
@testgear.description('E2E_autotest')
@testgear.labels('{labels}')
@testgear.link(url='https://roviti2348.atlassian.net/browse/JCP-15593')
@testgear.link(url='{url}', type='{link_type}', title='{link_title}')
@pytest.mark.parametrize('name, labels, url, link_type, link_title', [
    ('param 1', ['E2E', 'test'], 'https://dumps.example.com/module/JCP-15593', testgear.LinkType.DEFECT, 'JCP-15593'),
    ('param 2', (), 'https://github.com/testgear-tms/listener-csharp', testgear.LinkType.RELATED, 'Listener'),
    ('param 3', ('E2E', 'test'), 'https://best-tms.testgear.software/projects', testgear.LinkType.REQUIREMENT, ''),
    ('param 4', {'E2E', 'test'}, 'https://testgear.software/', testgear.LinkType.BLOCKED_BY, 'TestGear'),
    ('param 5', 'test', 'https://github.com/testgear-tms', testgear.LinkType.REPOSITORY, 'GitHub')
])
def test_1(self, name, labels, url, link_type, link_title):
    testgear.addLink(
        title='component_dump.dmp',
        type=testgear.LinkType.RELATED,
        url='https://dumps.example.com/module/some_module_dump'
    )
    testgear.addLink(
        title='component_dump.dmp',
        type=testgear.LinkType.BLOCKED_BY,
        url='https://dumps.example.com/module/some_module_dump'
    )
    testgear.addLink(
        title='component_dump.dmp',
        type=testgear.LinkType.DEFECT,
        url='https://dumps.example.com/module/some_module_dump'
    )
    testgear.addLink(
        title='component_dump.dmp',
        type=testgear.LinkType.ISSUE,
        url='https://dumps.example.com/module/some_module_dump'
    )
    testgear.addLink(
        title='component_dump.dmp',
        type=testgear.LinkType.REQUIREMENT,
        url='https://dumps.example.com/module/some_module_dump'
    )
    testgear.addLink(
        title='component_dump.dmp',
        type=testgear.LinkType.REPOSITORY,
        url='https://dumps.example.com/module/some_module_dump'
    )
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
        testgear.attachments(
            join(dirname(__file__), 'docs/text_file.txt'),
            join(dirname(__file__), 'pictures/picture.jpg'),
            join(dirname(__file__), 'docs/document.docx')
        )
        testgear.attachments(
            join(dirname(__file__), 'docs/document.doc'),
            join(dirname(__file__), 'docs/logs.log')
        )
        assert True
```

# Contributing

You can help to develop the project. Any contributions are **greatly appreciated**.

* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/testgear-tms/adapters-python/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/testgear-tms/adapters-python/blob/master/CODE_OF_CONDUCT.md) before posting your first idea as well.

# License

Distributed under the Apache-2.0 License. See [LICENSE](https://github.com/testgear-tms/adapters-python/blob/master/LICENSE.md) for more information.

