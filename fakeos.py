"""Full mock of the builtin 'os' module for blazing-fast unit-testing."""
from pathlib import Path

from environment import FakeEnvironment
from filesystem import FakeFilesystem


class FakeOS(object):
    """I mock the 'os' module"""
    # pylint: disable=too-few-public-methods
    def __init__(self, cwd: Path = None,
                 filesystem: FakeFilesystem = None,
                 environment: FakeEnvironment = None):

        self.cwd = cwd or Path(__file__)
        self.filesystem = filesystem or FakeFilesystem()
        self.environment = environment or FakeEnvironment()

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

    def environ(self) -> dict:
        """A dictionary representing the string environment.
        For example, environ['HOME'] is the pathname of your home directory
        (on some platforms), and is equivalent to getenv("HOME") in C.
        This mapping is captured the first time the os module is imported,
        typically during Python startup as part of processing site.py.
        Changes to the environment made after this time are not reflected in
        os.environ, except for changes made by modifying os.environ directly."""
        return self.environment.environ()

    def getenv(self, key: str, default: str = None) -> str:
        """Return the value of the environment variable key if it exists,
        or default if it doesn’t. key, default and the result are str."""
        return self.environment.getenv(key, default)

    def putenv(self, key: str, value: str):
        """Set the environment variable named key to the string value.
        Such changes to the environment affect subprocesses started with
        os.system(), popen() or fork() and execv().
        Availability: most flavors of Unix, Windows.

        Note:
             On some platforms, including FreeBSD and Mac OS X, setting
             environ may cause memory leaks. Refer to the system documentation
             for putenv.
        """
        self.environment.putenv(key, value)
