"""Everything related to operating system types and flavors."""
# pylint: disable=invalid-name
from abc import ABC, abstractmethod
from collections import namedtuple

uname_result = namedtuple('uname_result', ['sysname', 'nodename',
                                           'release', 'version', 'machine'])

class FakeOperatingSystem(ABC):
    """An abstract operating system"""
    # pylint: disable=too-few-public-methods
    def __init__(self, cpu_count: int = 1):
        self.cpu_count = cpu_count

    @abstractmethod
    def uname(self) -> uname_result:
        """Return the uname of the operating system."""
        pass

class FakeUnix(FakeOperatingSystem):
    """Unix operating system"""
    # pylint: disable=too-few-public-methods,too-many-arguments
    def __init__(self, cpu_count: int = 1,
                 sysname: str = "",
                 nodename: str = "",
                 release: str = "",
                 version: str = "",
                 machine: str = ""):
        super().__init__(cpu_count=cpu_count)
        self.sysname = sysname
        self.nodename = nodename
        self.release = release
        self.version = version
        self.machine = machine

    def uname(self) -> uname_result:
        return uname_result(sysname=self.sysname,
                            nodename=self.nodename,
                            release=self.release,
                            version=self.version,
                            machine=self.machine)


class FakeWindows(FakeOperatingSystem):
    """Windows operating system"""
    # pylint: disable=too-few-public-methods
    def uname(self):
        raise AttributeError("'module' object has no attribute 'uname'")
