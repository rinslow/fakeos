import os as _os

from pathlib import Path
from string import ascii_letters

from fakeos import FakeOS
from hypothesis import given, assume, example
from hypothesis.strategies import text, sets, integers

from filesystem import FakeDirectory, FakeFile, FakeFilesystem, \
    FakeFilesystemWithPermissions
from fakeuser import FakeUser
from unittest import TestCase

from operating_system import Windows, Unix

ILLEGAL_NAMES = ("", ".", "..")


class DirectoryCase(TestCase):
    @given(text())
    def test_mkdir_when_directory_already_exists(self, directory: str):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)

        with self.assertRaises(FileExistsError):
            os.mkdir("/" + directory)

    @given(text())
    def test_mkdir_when_parent_directory_doesnt_exist(self, directory: str):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))

        with self.assertRaises(FileNotFoundError):
            os.mkdir("/hello/" + directory)

    @given(text(), text())
    def test_mkdir_and_directory_exists_afterwards(self, directory: str, _file: str):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)
        assume("/" not in _file and _file not in ILLEGAL_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)
        os.mkdir("/" + directory + "/" + _file)

        assert os.filesystem.has(Path("/" + directory + "/" + _file))

    @given(text())
    def test_mkdir_works(self, directory):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)
        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)

    @given(text())
    def test_creating_root_directory(self, directory):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)
        os = FakeOS()
        os.mkdir(directory)

        assert os.filesystem.has_directory(Path(directory))

    @given(text(), sets(text()))
    @example("0", set())
    def test_listdir_with_subdirectories_only(self, directory, subdirectories):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)

        for subdirectory in subdirectories:
            assume(subdirectory not in ILLEGAL_NAMES)
            assume("/" not in subdirectory)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)

        for subdirectory in subdirectories:
            os.mkdir("/" + directory + "/" + subdirectory)

        assert sorted(subdirectories) == sorted(os.listdir("/" + directory))

    @given(text())
    def test_listdir_empty_directory(self, directory):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))

        os.mkdir("/" + directory)

        assert os.listdir("/" + directory) == []

    @given(text(), text())
    def test_listdir_with_a_file_inside(self, directory, filename):
        assume("/" not in directory and directory not in ILLEGAL_NAMES)
        assume("/" not in filename and filename not in ILLEGAL_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))],
                                      files=[FakeFile(Path("/" +
                                                        directory +
                                                        "/" +
                                                        filename))]
                                      ))

        os.mkdir("/" + directory)

        assert os.listdir("/" + directory) == [filename]


    @given(text(), text(), text())
    def test_listdir_with_a_file_and_a_directory_inside(self, directory,
                                                        filename, subdirectory):
        assume(subdirectory != filename)
        assume("/" not in directory and directory not in ILLEGAL_NAMES)
        assume("/" not in filename and filename not in ILLEGAL_NAMES)
        assume("/" not in subdirectory and subdirectory not in ILLEGAL_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))],
                                      files=[FakeFile(Path("/" +
                                                        directory +
                                                        "/" +
                                                        filename))]
                                      ))

        os.mkdir("/" + directory)
        os.mkdir("/" + directory + "/" + subdirectory)

        assert sorted(os.listdir("/" + directory)) == sorted([filename, subdirectory])

    @given(text())
    def test_makedirs_one_file_path(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path(path))]))
        with self.assertRaises(OSError):
            os.makedirs(path)

        try:
            os.makedirs(path, exist_ok=True)

        except OSError:
            self.fail()

    @given(text())
    @example("/")
    @example("/0")
    def test_makedirs_multiple_file_path(self, path: str):
        assume("/" in path and not path.startswith("."))
        os = FakeOS()
        os.makedirs(path)

        with self.assertRaises(OSError):
            os.makedirs(path)

    @given(text())
    def test_makedirs_when_part_of_the_path_exists_as_and_is_a_file(self, path: str):
        assume("/" in path)
        os = FakeOS(filesystem=FakeFilesystem(files=[FakeFile(Path(path))]))
        dirname = Path(path).joinpath("dirname")

        with self.assertRaises(FileExistsError):
            os.makedirs(dirname)

    @given(text())
    @example("0")
    def test_rmdir(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS()
        fullpath = "/" + path
        os.makedirs(fullpath)
        assert path in os.listdir("/")

        os.rmdir(fullpath)
        assert path not in os.listdir("/")

        with self.assertRaises(FileNotFoundError):
            os.rmdir(fullpath)

        os.makedirs(fullpath + "/hello")

        with self.assertRaises(OSError):
            os.rmdir(fullpath)

        os = FakeOS(filesystem=FakeFilesystemWithPermissions(FakeFilesystem(
            files=[FakeFile(Path(path))])))

        with self.assertRaises(NotADirectoryError):
            os.rmdir(path)


class ChownCase(TestCase):
    @given(text(), integers(), integers())
    def test_chown_to_a_directory(self, path: str, uid: int, gid: int):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS()
        os.mkdir(path)
        os.chown(path, uid=uid, gid=gid)

        assert os.filesystem[path].uid == uid
        assert os.filesystem[path].gid == gid

    @given(text(), integers(), integers())
    def test_chown_to_a_file(self, path: str, uid: int, gid: int):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS(filesystem=FakeFilesystem(files=[FakeFile(Path(path))]))
        os.chown(path, gid=gid, uid=uid)

        assert os.filesystem[path].uid == uid
        assert os.filesystem[path].gid == gid

    @given(text(), integers(), integers())
    def test_chown_to_a_nonexisting_fileobject(self, path: str, uid: int,
                                               gid: int):
        os = FakeOS()
        with self.assertRaises(FileNotFoundError):
            os.chown(path, gid=gid, uid=uid)

    @given(text(), integers(), integers())
    def test_chown_not_changing_already_set_attributes(self, path: str,
                                                       uid: int, gid: int):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS()
        os.mkdir(path)
        os.chown(path, uid=uid, gid=gid)
        os.chown(path, uid=-1, gid=-1)

        assert os.filesystem[path].gid == gid
        assert os.filesystem[path].uid == uid

    def test_chown_when_theres_no_permission_to_do_so(self):
        os = FakeOS(user=FakeUser(gid=2, uid=2, is_sudoer=False))
        os.mkdir("/", mode=0)  # Root only
        with self.assertRaises(PermissionError):
            os.chown('/', uid=3)


class ChmodCase(TestCase):
    @given(text(), integers())
    def test_chmod(self, path, mode):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS()
        os.mkdir(path)
        os.chmod(path, mode)

        assert os.filesystem[path].mode == mode


class FileCase(TestCase):
    @given(text())
    @example("0")
    def test_remove_a_file(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS(filesystem=FakeFilesystemWithPermissions(FakeFilesystem(
            files=[FakeFile(Path("hello/" + path))])))
        os.mkdir("hello")

        assert os.listdir("hello") == [path]
        os.remove("hello/" + path)
        assert os.listdir("hello") == []

    @given(text())
    def test_remove_a_directory(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS()
        os.mkdir(path)

        with self.assertRaises(IsADirectoryError):
            os.remove(path)

    @given(text())
    def test_remove_a_non_existent_file(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)
        os = FakeOS()

        with self.assertRaises(FileNotFoundError):
            os.remove(path)


class CurrentDirectoryCase(TestCase):
    @given(text())
    def test_chdir(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)

        os = FakeOS()
        os.mkdir(path)
        os.chdir(path)
        assert os.getcwd() == str(Path(path).absolute())

    @given(text())
    def test_chdir_directory_does_not_exist(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)

        os = FakeOS()
        with self.assertRaises(FileNotFoundError):
            os.chdir(path)

    @given(text())
    def test_chdir_directory_path_is_a_file(self, path):
        assume("/" not in path and path not in ILLEGAL_NAMES)

        os = FakeOS(filesystem=FakeFilesystem(files=[FakeFile(Path(path))]))
        with self.assertRaises(NotADirectoryError):
            os.chdir(path)

class DeviceCase(TestCase):
    @given(integers(), integers())
    def test_makedev(self, major, minor):
        assume(-1 < major < 2 ** 31 and -1  < minor < 2 ** 31)
        os = FakeOS()
        assert os.makedev(major, minor) == _os.makedev(major, minor)

    @given(integers())
    def test_major(self, device):
        assume(-1 < device < 2 ** 64)
        os = FakeOS()
        assert os.major(device) == _os.major(device)

    @given(integers())
    def test_minor(self, device):
        assume(-1 < device < 2 ** 64)
        os = FakeOS()
        assert os.minor(device) == _os.minor(device)


class RenameCase(TestCase):
    @given(text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1))
    def test_renaming_root_directory(self, old, new):
        assume(old != new)
        os = FakeOS()
        os.mkdir(old)

        os.rename(old, new)

        with self.assertRaises(FileNotFoundError):
            old_file = os.filesystem[Path(old)]

        try:
            new_file = os.filesystem[Path(new)]

        except FileNotFoundError:
            self.fail("Filke was not renamed.")

    @given(text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1))
    def test_renaming_non_root_directory(self, root, old, new):
        os = FakeOS()
        os.mkdir(root)
        os.mkdir(root + "/" + old)

        os.rename(root + "/" + old, root + "/" + new)

        assert os.listdir(root) == [new]

    @given(text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1))
    def test_renaming_root_non_leaf_folder(self, old, new, inside):
        os = FakeOS()
        os.mkdir(old)
        os.mkdir(old + "/" + inside)

        os.rename(old, new)
        assert os.listdir(new) == [inside]

    @given(text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1))
    def test_renaming_non_root_non_leaf_folder(self, old, new, inside, root):
        os = FakeOS()
        os.makedirs(root + "/" + old + "/" + inside)

        os.rename(root + "/" + old, root + "/" + new)

        assert os.listdir(root + "/" + new) == [inside]

    @given(text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1))
    def test_renaming_when_destination_exists_on_windows(self, old, new):
        assume(old != new)

        os = FakeOS(operating_system=Windows())
        os.mkdir(old)
        os.mkdir(new)

        with self.assertRaises(OSError):
            os.rename(old, new)

    @given(text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1))
    def test_renaming_when_destination_exists_on_unix(self, old, new, somefile):
        assume(old != new)

        os = FakeOS(operating_system=Unix(),
                    filesystem=FakeFilesystem(files=[FakeFile(Path(old)),
                                                     FakeFile(Path(new))],
                                              operating_system=Unix()))

        os.rename(old, new)
        os.filesystem[Path(new)]

        with self.assertRaises(OSError):
            fileobject = os.filesystem[Path(old)]

    @given(text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1),
           text(alphabet=ascii_letters, min_size=1))
    def test_renaming_a_folder_and_changing_its_hierarchy(self, a, b, c, d, e):
        assume(e != b)
        os = FakeOS()
        os.makedirs(a + "/" + b + "/" + c + "/" + d)

        os.rename(a + "/" + b + "/" + c, a + "/" + e)

        assert set(os.listdir(a)) == {b, e}
        assert os.listdir(a + "/" + e) == [d]

    @given(text(alphabet=ascii_letters, min_size=1))
    def test_renaming_to_the_same_thing(self, path):
        os = FakeOS()
        os.mkdir(path)
        os.rename(path, path)


class PermissionsCase(TestCase):
    def test_rmdir_when_theres_no_permission_to_do_so(self):
        os = FakeOS(user=FakeUser(uid=0, gid=0))
        os.mkdir("/", mode=0)
        with self.assertRaises(PermissionError):
            os.rmdir("/")

    def test_renaming_when_theres_no_permission_to_do_so(self):
        os = FakeOS(user=FakeUser())
        os.mkdir("/", mode=0o000)
        with self.assertRaises(PermissionError):
            os.rename("/", "lol")

    def test_chmod_when_theres_no_permission_to_do_so(self):
        os = FakeOS(user=FakeUser(gid=2, uid=2, is_sudoer=False))
        os.mkdir("/", mode=0o100)  # Root only
        with self.assertRaises(PermissionError):
            os.chmod("/", mode=0o666)
