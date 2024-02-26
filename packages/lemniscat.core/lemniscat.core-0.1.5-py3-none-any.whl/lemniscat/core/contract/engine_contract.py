from logging import Logger
from typing import Optional, List

from lemniscat.core.model import Meta, TaskResult
from lemniscat.core.util.helpers import Interpreter


class IPluginRegistry(type):
    plugin_registries: List[type] = list()

    def __init__(cls, name, bases, attrs):
        super().__init__(cls)
        if name != 'PluginCore':
            IPluginRegistry.plugin_registries.append(cls)


class PluginCore(object, metaclass=IPluginRegistry):
    """
    Plugin core class
    """

    meta: Optional[Meta]
    _interpreter: Interpreter
    
    variables: dict
    parameters: dict

    def __init__(self, logger: Logger) -> None:
        """
        Entry init block for plugins
        :param logger: logger that plugins can make use of
        """
        self.variables = {}
        self._logger = logger
        
    def info(self) -> None:
        """
        Show plugin meta information
        :return: Meta
        """
        self._logger.info('-----------------------------------------')
        self._logger.info(f'Name: {self.meta.name}')
        self._logger.info(f'Description: {self.meta.description}')
        self._logger.info(f'Version: {self.meta.version}')
        self._logger.info('-----------------------------------------')

    def invoke(self, parameters: dict = {}, variables: dict = {}) -> TaskResult:
        """
        Starts main plugin flow
        :param args: possible arguments for the plugin
        :return: a result for the plugin
        """
        self._interpreter = Interpreter(self._logger, variables)
        # interpret existing variables 
        self._interpreter.interpret()
        # interpret parameters
        parameters = self._interpreter.interpretParameters(parameters)
        
    
    def appendVariables(self, variables: dict) -> None:
        self._logger.debug(f"Append {len(variables)} variables")
        self.variables.update(variables)
        self._logger.debug(f"Now, there are {len(self.variables)} variables provided by this task")
        
    def getVariables(self) -> dict:
        return self.variables