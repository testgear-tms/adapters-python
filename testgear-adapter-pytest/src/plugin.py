import testgear_adapter_pytest
import pytest
from testgear_adapter_pytest.listener import PluginListener


def pytest_addoption(parser):
    parser.getgroup('testgear').addoption(
        '--testgear',
        action='store_true',
        dest="testgear_report",
        help='Pytest plugin for TestGear'
    )
    parser.getgroup('testgear').addoption(
        '--testrunid',
        action="store",
        dest="set_testrun",
        metavar="5236eb3f-7c05-46f9-a609-dc0278896464",
        help='Set Test-run ID'
    )
    parser.getgroup('testgear').addoption(
        '--testgear_url',
        action="store",
        dest="set_url",
        metavar="https://demo.testgear.software",
        help='Set location of the TestGear instance'
    )
    parser.getgroup('testgear').addoption(
        '--privatetoken',
        action="store",
        dest="set_privatetoken",
        metavar="T2lKd2pLZGI4WHRhaVZUejNl",
        help='Set API secret key'
    )
    parser.getgroup('testgear').addoption(
        '--configurationid',
        action="store",
        dest="set_configurationid",
        metavar="d354bdac-75dc-4e3d-84d4-71186c0dddfc",
        help='Set Configuration ID'
    )
    parser.getgroup('debug').addoption(
        '--testgear_proxy',
        action="store",
        dest="set_testgear_proxy",
        metavar='{"http":"http://localhost:8888","https":"http://localhost:8888"}',
        help='Set proxy for sending requests'
    )


@pytest.mark.tryfirst
def pytest_cmdline_main(config):
    if config.option.testgear_report:
        listener = PluginListener(config.option.set_testrun,
                                      config.option.set_url,
                                      config.option.set_privatetoken,
                                      config.option.set_configurationid,
                                      config.option.set_testgear_proxy)
        config.pluginmanager.register(listener)
        testgear_adapter_pytest.LocalPluginManager.get_plugin_manager().register(listener)
