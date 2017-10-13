"""Everything needed for being able to create a virtual filesystem."""
import typing
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path

from operating_system import OperatingSystem, Unix, Windows
from fakeuser import FakeUser, Root


class FakeFileLikeObject(ABC):
    """I am what's common between a file, a directory, a symlink and a mount."""
    def __init__(self, path: Path,
                 mode: int = 0o777,
                 uid: int = -1,
                 gid: int = -1):
        self.path = path
        self.uid = uid
        self.gid = gid
        self.mode = mode

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
    pass


class FakeDirectory(FakeFileLikeObject):
    """I mock a directory."""
    def parts(self) -> typing.List[Path]:
        """returns the parts the directory is made of"""
        path_so_far = Path()
        for part in self.path.parts:
            path_so_far = path_so_far.joinpath(part)
            yield path_so_far


class AbstractFilesystem(ABC):
    # pylint: disable=missing-docstring
    @abstractmethod
    def has_directory(self, path: Path) -> bool:
        pass

    @abstractmethod
    def has_file(self, path: Path) -> bool:
        pass

    @abstractmethod
    def has(self, path: Path) -> bool:
        pass

    @abstractmethod
    def mkdir(self, path: Path, mode: int):
        pass

    @abstractmethod
    def makedirs(self, path: Path, mode: int, exist_ok: bool):
        pass

    @abstractmethod
    def listdir(self, path: Path) -> typing.Iterator[FakeFileLikeObject]:
        pass

    @abstractmethod
    def chown(self, path: Path, uid: int, gid: int):
        pass

    @abstractmethod
    def chmod(self, path: Path, mode: int):
        pass

    @abstractmethod
    def rmdir(self, path: Path):
        pass

    @abstractmethod
    def remove(self, path: Path):
        pass

    @abstractmethod
    def rename(self, src: Path, dst: Path):
        pass

    @abstractproperty
    def user(self) -> FakeUser:
        pass

    @abstractmethod
    def access(self, path: Path, mode: int):
        pass

    @abstractmethod
    def set_user(self, user: FakeUser):
        pass

class FakeFilesystem(AbstractFilesystem):
    """I mock the behaviour of an entire filesystem."""
    def __init__(self,
                 directories=None,
                 files=None,
                 operating_system: OperatingSystem = None,
                 user: FakeUser = None):

        self.directories = directories or list()
        self.files = files or list()
        self._user = user or Root()
        self.operating_system = operating_system or Unix()

    def __getitem__(self, path: Path) -> FakeFileLikeObject:
        if isinstance(path, str):
            path = Path(path)

        for file_object in self:
            if file_object.path.absolute() == path.absolute():
                return file_object

        raise FileNotFoundError(path)

    def __iter__(self) -> typing.Iterator[FakeFileLikeObject]:
        return iter(self.directories + self.files)

    @property
    def user(self):
        return self._user

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

        if (path.parent != self.curdir and
                path.parent != path and not self.has(path.parent)):
            raise FileNotFoundError

        self.directories.append(FakeDirectory(path,
                                              mode,
                                              uid=self.user.uid,
                                              gid=self.user.gid)
                               )

    def makedirs(self, path: Path, mode: int = 0o777, exist_ok=False):
        """Recursively make path to a directory."""
        if self.has(path) and not exist_ok:
            raise OSError(path)

        for part in FakeDirectory(path).parts():
            if self.has_file(part):
                raise FileExistsError

            if not self.has_directory(part):
                self.mkdir(part, mode)

    def has_directory(self, path: Path) -> bool:
        """Whether or not such a directory exists."""
        return path.absolute() in (d.path.absolute() for d in self.directories)

    def has_file(self, path: Path) -> bool:
        """Whether or not such a file exists."""
        return path.absolute() in (f.path.absolute() for f in self.files)

    def listdir(self, path: Path) -> typing.Iterator[FakeFileLikeObject]:
        """List all files in a directory"""
        for file_object in self:
            if file_object.parent.absolute() == path.absolute():
                yield file_object

    def chown(self, path: Path, uid: int = -1, gid: int = -1):
        """Change the ownership of a file."""
        if uid != -1:
            self[path].uid = uid

        if gid != -1:
            self[path].gid = gid

    def chmod(self, path: Path, mode: int):
        """Chnage the mode of a file."""
        if not isinstance(mode, int):
            raise TypeError(mode)

        self[path].mode = mode

    def rmdir(self, path: Path):
        """Remove a directory."""
        if self.has_file(path):
            raise NotADirectoryError(path)

        if not self.has_directory(path):
            raise FileNotFoundError(path)

        if list(self.listdir(path)):
            raise OSError(path)

        for directory in self.directories:
            if directory.path.absolute() == path.absolute():
                self.directories.remove(directory)

    def remove(self, path: Path):
        """Remove a file."""
        if self.has_directory(path):
            raise IsADirectoryError(path)

        if not self.has_file(path):
            raise FileNotFoundError(path)

        for file in self.files:
            if file.path.absolute() == path.absolute():
                self.files.remove(file)

    def rename(self, src: Path, dst: Path):
        """Rename a file."""
        if src == dst:
            return

        if self.has_directory(dst):
            raise FileExistsError(dst)

        if isinstance(self.operating_system, Windows) and self.has(dst):
            raise FileExistsError(dst)

        self[src].path = dst

        for file_object in self:
            if src in file_object.path.parents:
                file_object.path = dst / file_object.path.relative_to(src)

    def access(self, path: Path, mode: int):
        """Test access for a file object."""
        if mode == 0:
            return self.has(path)

        return self.user.can_access(self[path], action_mask=mode)

    def set_user(self, user: FakeUser):
        """Set the user."""
        self._user = user


class FakeFilesystemWithPermissions(AbstractFilesystem):
    """A filesystem decorator implementing user permissions.

    Attributes:
        filesystem (FakeFilesystem): encapsulated file system.
    """
    def __init__(self, filesystem: AbstractFilesystem):
        self.filesystem = filesystem

    def __getitem__(self, item):
        return self.filesystem[item]

    def __iter__(self):
        return iter(self.filesystem)

    def chown(self, path: Path, uid: int = -1, gid: int = -1):
        if not self.user.can_write(self[path]):
            raise PermissionError(path)

        return self.filesystem.chown(path=path, uid=uid, gid=gid)

    def chmod(self, path: Path, mode: int):
        if not self.user.can_write(self[path]):
            raise PermissionError(path)

        return self.filesystem.chmod(path=path, mode=mode)

    def mkdir(self, path: Path, mode: int = 0o777):
        if self.has_directory(path.parent) and not self.user.can_write(
                self[path.parent]):
            raise PermissionError(path.parent)

        return self.filesystem.mkdir(path=path, mode=mode)

    def listdir(self, path: Path):
        if not self.user.can_execute(self[path]):
            raise PermissionError(path)

        return self.filesystem.listdir(path=path)

    def rmdir(self, path: Path):
        if not self.user.can_write(self[path]):
            raise PermissionError(path)

        return self.filesystem.rmdir(path=path)

    def remove(self, path: Path):
        if not self.user.can_write(self[path]):
            raise PermissionError(path)

        return self.filesystem.remove(path=path)

    def rename(self, src: Path, dst: Path):
        if not self.user.can_write(self[src]):
            raise PermissionError(src)

        if self.has_directory(dst.parent) and not self.user.can_write(
                self[dst.parent]):
            raise PermissionError(dst)

        return self.filesystem.rename(src=src, dst=dst)

    def has(self, path: Path) -> bool:
        return self.filesystem.has(path=path)

    def makedirs(self, path: Path, mode: int = 0o777, exist_ok: bool = False):
        return self.filesystem.makedirs(path=path, mode=mode, exist_ok=exist_ok)

    @property
    def user(self):
        return self.filesystem.user

    def has_directory(self, path: Path) -> bool:
        return self.filesystem.has_directory(path=path)

    def has_file(self, path: Path) -> bool:
        return self.filesystem.has_file(path=path)

    def access(self, path: Path, mode: int):
        return self.filesystem.access(path=path, mode=mode)

    def set_user(self, user: FakeUser):
        return self.filesystem.set_user(user)
