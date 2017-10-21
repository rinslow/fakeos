"""Full mock of the builtin 'os' module for blazing-fast unit-testing."""
# pylint: disable=import-self
from fakeos import FakeOS
from filesystem import (FakeFilesystem, FakeDirectory, FakeFile,
                        FakeFilesystemWithPermissions)
from environment import FakeEnvironment
from device import FakeDevice
from fakeuser import FakeUser, Root
from operating_system import FakeUnix, FakeWindows
