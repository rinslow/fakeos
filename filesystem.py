"""Everything needed for being able to create a virtual filesystem."""
from pathlib import Path


class FakeFile(object):
    """I mock a file"""
    # pylint: disable=too-few-public-methods
    def __init__(self, path: Path, mode: int = 0o77):
        self.path = path
        self.mode = mode


class FakeDirectory(object):
    """I mock a directory."""
    # pylint: disable=too-few-public-methods
    def __init__(self, path: Path, mode: int = 0o777):
        self.path = path
        self.mode = mode


class FakeFilesystem(object):
    """I mock the behaviour of an entire filesystem."""
    def __init__(self, directories=None, files=None):
        self.directories = directories or list()
        self.files = files or list()

    def mkdir(self, path: Path, mode: int = 0o777):
        """Create an empty directory."""
        if self.has(path):
            raise FileExistsError

        if not self.has(path.parent):
            raise FileNotFoundError

        self.directories.append(FakeDirectory(path, mode))

    def has(self, path) -> bool:
        """Whether or not path already exists"""
        return any([path.absolute() in (d.path.absolute() for d in self.directories),
                    path.absolute() in (f.path.absolute() for f in self.files)])
