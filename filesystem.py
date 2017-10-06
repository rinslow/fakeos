"""Everything needed for being able to create a virtual filesystem."""
import typing
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

    def parts(self) -> typing.List[Path]:
        """returns the parts the directory is made of"""
        path_so_far = Path()
        for part in self.path.parts:
            path_so_far = path_so_far.joinpath(part)
            yield path_so_far


class FakeFilesystem(object):
    """I mock the behaviour of an entire filesystem."""
    def __init__(self, directories=None, files=None):
        self.directories = directories or list()
        self.files = files or list()

    @property
    def curdir(self):
        """Return a path representing the current directory."""
        return Path(".")

    def has(self, path) -> bool:
        """Whether or not path already exists"""
        return self.has_directory(path) or self.has_file(path)

    def mkdir(self, path: Path, mode: int = 0o777):
        """Create an empty directory."""
        if self.has(path):
            raise FileExistsError

        if path.parent != self.curdir and path.parent != path and not self.has(path.parent):
            raise FileNotFoundError

        self.directories.append(FakeDirectory(path, mode))

    def makedirs(self, path: Path, mode: int = 0o777, exist_ok=False):
        """Recursively make path to a directory."""
        if self.has(path) and not exist_ok:
            raise OSError(path)

        for part in FakeDirectory(path).parts():
            if self.has_file(part):
                raise FileExistsError

            if not self.has_directory(part):
                self.mkdir(part, mode)


    def has_directory(self, path) -> bool:
        """Whether or not such a directory exists."""
        return path.absolute() in (d.path.absolute() for d in self.directories)

    def has_file(self, path) -> bool:
        """Whether or not such a file exists."""
        return path.absolute() in (f.path.absolute() for f in self.files)

    def listdir(self, path: Path) -> [str]:
        """List all files in a directory"""
        for file_object in self.files + self.directories:
            if file_object.parent.absolute() == path.absolute():
                yield file_object.name
