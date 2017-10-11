"""Everything related to operating system types and flavors."""
from abc import ABC


class OperatingSystem(ABC):
    """An abstract operating system"""
    # pylint: disable=too-few-public-methods
    pass


class Unix(OperatingSystem):
    """Unix operating system"""
    # pylint: disable=too-few-public-methods
    pass


class Windows(OperatingSystem):
    """Windows operating system"""
    # pylint: disable=too-few-public-methods
    pass
