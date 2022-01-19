from pluggy import PluginManager


class LocalPluginManager:
    plugin_manager = None

    @classmethod
    def get_plugin_manager(cls):
        if not cls.plugin_manager:
            cls.plugin_manager = PluginManager('testgear')
        return cls.plugin_manager

    @classmethod
    def __getattr__(cls, attribute):
        return getattr(cls.get_plugin_manager(), attribute)
