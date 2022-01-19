from testgear_adapter_pytest.plugin_manager import LocalPluginManager
from pluggy import HookimplMarker

hookimpl = HookimplMarker("testit")

__all__ = [
    'LocalPluginManager',
    'hookimpl'
]
