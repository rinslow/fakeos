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

    def listdir(self, path: str) -> list:
        """Return a list containing the names of the entries in the directory
        given by path. The list is in arbitrary order, and does not include the
        special entries '.' and '..' even if they are present in the
        directory."""
        file_objects = self.filesystem.listdir(Path(path))
        return [file_object.name for file_object in file_objects]

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

    def makedirs(self, name, mode: int = 0o77, exist_ok: bool = False):
        """Recursive directory creation function.
        Like mkdir(), but makes all intermediate-level directories needed
        to contain the leaf directory. The mode parameter is passed to mkdir()
        see the mkdir() description for how it is interpreted.
        If exist_ok is False (the default), an OSError is raised if the
        target directory already exists.
         """
        self.filesystem.makedirs(Path(name), mode=mode, exist_ok=exist_ok)

    def chown(self, path: str, uid: int = -1, gid: int = -1):
        """Change the owner and group id of path to the numeric uid and gid.
        To leave one of the ids unchanged, set it to -1.
        Availability: Unix.
        """
        self.filesystem.chown(Path(path), uid, gid)

    def chmod(self, path: str, mode: int):
        """"Change the mode of path to the numeric mode.
        mode may take one of the following values (as defined in
        the stat module) or bitwise ORed combinations of them:
            stat.S_ISUID
            stat.S_ISGID
            stat.S_ENFMT
            stat.S_ISVTX
            stat.S_IREAD
            stat.S_IWRITE
            stat.S_IEXEC
            stat.S_IRWXU
            stat.S_IRUSR
            stat.S_IWUSR
            stat.S_IXUSR
            stat.S_IRWXG
            stat.S_IRGRP
            stat.S_IWGRP
            stat.S_IXGRP
            stat.S_IRWXO
            stat.S_IROTH
            stat.S_IWOTH
            stat.S_IXOTH"""
        self.filesystem.chmod(Path(path), mode)

    def rmdir(self, path: str):
        """Remove (delete) the directory path. Only works when the directory
        is empty, otherwise, OSError is raised. """
        return self.filesystem.rmdir(Path(path))

    def remove(self, path: str):
        """Remove (delete) the file path. If path is a directory,
        OSError is raised. Use rmdir() to remove directories.
        This function is semantically identical to unlink()."""
        self.filesystem.remove(Path(path))

    def unlink(self, path: str):
        """Remove (delete) the file path. This function is semantically
        identical to remove(); the unlink name is its traditional Unix name.
        Please see the documentation for remove() for further information."""
        self.remove(path)
