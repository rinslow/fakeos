"""Everything needed for being able to create a virtual filesystem."""
from pathlib import Path


class FakeFileLikeObject(object):
    """I am what's common between a file, a directory, a symlink and a mount."""
    def __init__(self, path: Path):
        self.path = path

    @property
    def parent(self) -> Path:
        """Return this file-like object's parent."""
        return self.path.parent

    @property
    def name(self) -> str:
        """Return this file-like object's name"""
        return self.path.absolute().name


class FakeFile(FakeFileLikeObject):
    """I mock a file"""
    # pylint: disable=too-few-public-methods
    def __init__(self, path: Path, mode: int = 0o77):
        super(FakeFile, self).__init__(path=path)
        self.mode = mode


class FakeDirectory(FakeFileLikeObject):
    """I mock a directory."""
    # pylint: disable=too-few-public-methods
    def __init__(self, path: Path, mode: int = 0o777):
        super(FakeDirectory, self).__init__(path=path)
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

    def listdir(self, path: Path) -> list:
        """List all files in a directory"""
        for file_object in self.files + self.directories:
            if file_object.parent.absolute() == path.absolute():
                yield file_object.name
