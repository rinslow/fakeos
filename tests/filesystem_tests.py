from pathlib import Path

from fakeos import FakeOS, FakeFilesystem
from hypothesis import given, assume
from hypothesis.strategies import text

from filesystem import FakeDirectory
from unittest import TestCase


class DirectoryCase(TestCase):
    @given(text())
    def test_mkdir_when_directory_already_exists(self, path: str):
        assume("/" not in path)
        assume(path not in ("", "."))

        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + path)

        with self.assertRaises(FileExistsError):
            os.mkdir("/" + path)

    @given(text())
    def test_mkdir_when_parent_directory_doesnt_exist(self, path: str):
        assume("/" not in path)
        assume(path not in ("", "."))

        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))

        with self.assertRaises(FileNotFoundError):
            os.mkdir("/hello/" + path)

    @given(text(), text())
    def test_mkdir_and_directory_exists_afterwards(self, dir: str, _file: str):
        assume("/" not in dir)
        assume(dir not in ("", "."))

        assume("/" not in _file)
        assume(_file not in ("", "."))

        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + dir)
        os.mkdir("/" + dir + "/" + _file)

        assert os.filesystem.has(Path("/" + dir + "/" + _file))

    @given(text())
    def test_mkdir_works(self, directory_name):
        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        assume("/" not in directory_name)
        assume(directory_name not in (".", "..", ""))
        os.mkdir("/" + directory_name)


class CurrentDirectoryCase(TestCase):
    @given(text())
    def test_change_dir(self, path):
        os = FakeOS()
        os.chdir(path)
        assert os.getcwd() == str(Path(path).absolute())