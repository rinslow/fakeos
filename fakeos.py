"""Full mock of the builtin 'os' module for blazing-fast unit-testing."""
from pathlib import Path

from filesystem import FakeFilesystem


class FakeOS(object):
    """I mock the 'os' module"""
    # pylint: disable=too-few-public-methods
    def __init__(self, filesystem: FakeFilesystem = None):
        self.filesystem = filesystem or FakeFilesystem()

    def mkdir(self, path: str, mode: int = 0o777):
        """Create a directory named path with numeric mode mode.

        If the directory already exists, FileExistsError is raised.
        If the parent directory does not exist, FileNotFound is raised.

        On some systems, mode is ignored.
        Where it is used, the current umask value is first masked out.
        If bits other than the last 9 (i.e. the last 3 digits of the
        octal representation of the mode) are set,
        their meaning is platform-dependent.
        On some platforms, they are ignored and you should call chmod()
        explicitly to set them."""
        self.filesystem.mkdir(Path(path), mode=mode)
