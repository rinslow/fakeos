"""Everything related to operating system types and flavors."""
from abc import ABC


class FakeOperatingSystem(ABC):
    """An abstract operating system"""
    # pylint: disable=too-few-public-methods
    def __init__(self, cpu_count: int = 1):
        self.cpu_count = cpu_count


class FakeUnix(FakeOperatingSystem):
    """Unix operating system"""
    # pylint: disable=too-few-public-methods
    pass


class FakeWindows(FakeOperatingSystem):
    """Windows operating system"""
    # pylint: disable=too-few-public-methods
    pass
