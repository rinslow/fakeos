"""Everything needed for being able to create a virtual device."""
import os as _os


class FakeDevice(object):
    """Provides an adapter behaviour to the device interface.

    As of now it is implemented using the builtin os module but as you can
    see from the simplicity of this interface it is highly replaceable."""
    def __init__(self, device):
        self.device = device

    @property
    def major(self) -> int:
        """Return the major number of the device"""
        return _os.major(self.device)

    @property
    def minor(self) -> int:
        """Return the minor number of the device"""
        return _os.minor(self.device)

    @staticmethod
    def from_major_and_minor(major: int, minor: int) -> 'FakeDevice':
        """Create a device from major and minor numbers."""
        return FakeDevice(_os.makedev(major, minor))
