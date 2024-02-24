"""
A high-performance data profiling library oriented towards exploratory data analysis
"""
from __future__ import annotations
import typing
from . import ac
from . import afd
from . import ar
from . import data_types
from . import fd
from . import fd_verification
from . import mfd_verification
from . import statistics
from . import ucc
from . import ucc_verification

__all__ = [
    "Algorithm",
    "ConfigurationError",
    "ac",
    "afd",
    "afd_verification",
    "ar",
    "data_types",
    "fd",
    "fd_verification",
    "mfd_verification",
    "statistics",
    "ucc",
    "ucc_verification",
]

class Algorithm:
    def execute(self, **kwargs) -> None:
        """
        Process data.
        """
    def get_description(self, option_name: str) -> str:
        """
        Get description of an option.
        """
    def get_needed_options(self) -> set[str]:
        """
        Get names of options the algorithm requires to be set at the moment.
        This option is only expected to be used by Python scripts in which it is
        easier to set all options one by one. For normal use, you may set the
        algorithms' options using keyword arguments of the load_data and execute
        methods.
        """
    def get_option_type(self, option_name: str) -> tuple:
        """
        Get info about the option's type.
        """
    def get_opts(self) -> dict[str, typing.Any]:
        """
        Get option values represented as the closest Python type
        """
    def get_possible_options(self) -> set[str]:
        """
        Get names of options the algorithm may request.
        """
    def load_data(self, **kwargs) -> None:
        """
        Load data for execution
        """
    def set_option(self, option_name: str, option_value: typing.Any = None) -> None:
        """
        Set option value. Passing None means setting the default value.
        This option is only expected to be used by Python scripts in which it is
        easier to set all options one by one. For normal use, you may set the
        algorithms' options using keyword arguments of the load_data and execute
        methods.
        """

class ConfigurationError(ValueError):
    pass

afd_verification = fd_verification
