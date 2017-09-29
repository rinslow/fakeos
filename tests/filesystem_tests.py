from pathlib import Path

from fakeos import FakeOS, FakeFilesystem
from hypothesis import given, assume, example
from hypothesis.strategies import text
import hypothesis.strategies

from filesystem import FakeDirectory
from unittest import TestCase


class DirectoryCase(TestCase):

    ILLEGAL_CHARS = ("", ".", "..")

    @given(text())
    def test_mkdir_when_directory_already_exists(self, path: str):
        assume("/" not in path)
        assume(path not in self.ILLEGAL_CHARS)

        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + path)

        with self.assertRaises(FileExistsError):
            os.mkdir("/" + path)

    @given(text())
    def test_mkdir_when_parent_directory_doesnt_exist(self, path: str):
        assume("/" not in path)
        assume(path not in self.ILLEGAL_CHARS)

        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))

        with self.assertRaises(FileNotFoundError):
            os.mkdir("/hello/" + path)

    @given(text(), text())
    def test_mkdir_and_directory_exists_afterwards(self, directory: str, _file: str):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_CHARS)

        assume("/" not in _file)
        assume(_file not in self.ILLEGAL_CHARS)

        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)
        os.mkdir("/" + directory + "/" + _file)

        assert os.filesystem.has(Path("/" + directory + "/" + _file))

    @given(text())
    def test_mkdir_works(self, directory_name):
        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        assume("/" not in directory_name)
        assume(directory_name not in self.ILLEGAL_CHARS)
        os.mkdir("/" + directory_name)

    @given(text(), hypothesis.strategies.sets(text()))
    @example("0", set())
    def test_listdir_with_subdirectories_only(self, directory, subdirectories):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_CHARS)
        for subdirectory in subdirectories:
            assume(subdirectory not in self.ILLEGAL_CHARS)
            assume("/" not in subdirectory)

        os = FakeOS(FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)

        for subdirectory in subdirectories:
            os.mkdir("/" + directory + "/" + subdirectory)

        assert sorted(subdirectories) == sorted(os.listdir("/" + directory))


class CurrentDirectoryCase(TestCase):
    @given(text())
    def test_change_dir(self, path):
        os = FakeOS()
        os.chdir(path)
        assert os.getcwd() == str(Path(path).absolute())
