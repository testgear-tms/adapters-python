# Test Gear TMS adapter for Behave

![Test Gear](https://raw.githubusercontent.com/testgear-tms/adapters-python/master/images/banner.png)

## Getting Started

### Installation

```
pip install testgear-adapter-behave
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
| It enables debug mode (**It's optional**)                                                                                                                                                                                                                                                                                                                                              | tmsProxy                   | TMS_PROXY                         | tmsProxy                      |
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
tmsProxy = {"http": "http://localhost:8888", "https": "http://localhost:8888"}
```

#### Examples

Launch with a connection_config.ini file in the root directory of the project:

```
$ behave -f testgear_adapter_behave.formatter:AdapterFormatter
```

Launch with command-line parameters:

```
$ behave -f testgear_adapter_behave.formatter:AdapterFormatter -D tmsUrl=URL -D tmsPrivateToken=USER_PRIVATE_TOKEN -D
tmsProjectId=PROJECT_ID -D tmsConfigurationId=CONFIGURATION_ID -D tmsTestRunId=TEST_RUN_ID -D tmsAdapterMode=ADAPTER_MODE -D
tmsTestRunName=TEST_RUN_NAME -D tmsProxy='{"http":"http://localhost:8888","https":"http://localhost:8888"}' -D
tmsCertValidation=CERT_VALIDATION -D tmsAutomaticCreationTestCases=AUTOMATIC_CREATION_TEST_CASES
```

If you want to enable debug mode then
see [How to enable debug logging?](https://github.com/testgear-tms/adapters-python/tree/main/testgear-python-commons)

### Tags

Use tags to specify information about autotest.

Description of tags:

- `WorkItemIds` - linking an autotest to a test case.
- `DisplayName` - name of the autotest in TMS.
- `ExternalId` - ID of the autotest within the project in TMS.
- `Title` - title in the autotest card.
- `Description` - description in the autotest card.
- `Labels` - tags in the autotest card.
- `Links` - links in the autotest card.
- `NameSpace` - directory in the TMS system (default - file's name of test)
- `ClassName` - subdirectory in the TMS system (default - class's name of test)

Description of methods:

- `testgear.addLinks` - links in the autotest result
- `testgear.addAttachments` - uploading files in the autotest result
- `testgear.addMessage` - information about autotest in the autotest result
- `testgear.step` - usage in the "with" construct to designation a step in the body of the test

### Examples

#### Simple Test

```py
import testgear
from behave import given
from behave import then
from behave import when


@given("I authorize on the portal")
def authorization(context):
    with testgear.step("I set login"):
        pass
    with testgear.step("I set password"):
        pass


@when("I create a project")
def create_project(context):
    pass


@when("I open the project")
def enter_project(context):
    pass


@when("I create a section")
def create_section(context):
    testgear.addLinks(
        title='component_dump.dmp',
        type=testgear.LinkType.RELATED,
        url='https://dumps.example.com/module/some_module_dump',
        description='Description'
    )


@then("I create a test case")
def create_test_case(context):
    testgear.addAttachments('pictures/picture.jpg')
```

```buildoutcfg
Feature: Sample

  Background:
    Given I authorize on the portal

  @ExternalId=failed_with_all_annotations
  @DisplayName=Failed_test_with_all_annotations
  @WorkItemIds=123
  @Title=Title_in_the_autotest_card
  @Description=Test_with_all_annotations
  @Labels=Tag1,Tag2
  @Links={"url":"https://dumps.example.com/module/repository","title":"Repository","description":"Example_of_repository","type":"Repository"}
  Scenario: Create new project, section and test case
    When I create a project
    And I open the project
    And I create a section
    Then I create a test case
```

#### Parameterized test

```py
from behave import when
from behave import then


@when("Summing {left:d}+{right:d}")
def step_impl(context, left, right):
    context.sum = left + right


@then("Result is {result:d}")
def step_impl(context, result):
    assert context.sum == result

```

```buildoutcfg
Feature: Rule
  Tests that use Rule

  Scenario Outline: Summing
    When Summing <left>+<right>
    Then Result is <result>

    Examples:
      | left | right | result |
      | 1    | 1     | 3      |
      | 9    | 9     | 18     |
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

