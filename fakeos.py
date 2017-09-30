"""Full mock of the builtin 'os' module for blazing-fast unit-testing."""
from pathlib import Path

from filesystem import FakeFilesystem


class FakeOS(object):
    """I mock the 'os' module"""
    # pylint: disable=too-few-public-methods
    def __init__(self,
                 filesystem: FakeFilesystem = None,
                 cwd: Path = None):

        self.filesystem = filesystem or FakeFilesystem()
        self.cwd = cwd or Path(__file__)

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

    def getcwd(self) -> str:
        """"Return a string representing the current working directory."""
        return str(self.cwd.absolute())

    def chdir(self, path: str):
        """Change the current working directory to path.
        If the directory does not exist FileNotFound is raised.
        If the file is not a directory, NotADirectory is raised."""
        if not self.filesystem.has(Path(path)):
            raise FileNotFoundError(path)

        if self.filesystem.has_file(Path(path)):
            raise NotADirectoryError(path)

        self.cwd = Path(path)

    def listdir(self, path: str) -> list:
        """Return a list containing the names of the entries in the directory
        given by path. The list is in arbitrary order, and does not include the
        special entries '.' and '..' even if they are present in the
        directory."""
        return list(self.filesystem.listdir(Path(path)))
