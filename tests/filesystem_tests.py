from pathlib import Path

from fakeos import FakeOS, FakeFilesystem
from hypothesis import given, assume, example
from hypothesis.strategies import text, sets

from filesystem import FakeDirectory, FakeFile
from unittest import TestCase


class DirectoryCase(TestCase):
    ILLEGAL_DIRECTORY_NAMES = ("", ".", "..")

    @given(text())
    def test_mkdir_when_directory_already_exists(self, directory: str):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)

        with self.assertRaises(FileExistsError):
            os.mkdir("/" + directory)

    @given(text())
    def test_mkdir_when_parent_directory_doesnt_exist(self, directory: str):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))

        with self.assertRaises(FileNotFoundError):
            os.mkdir("/hello/" + directory)

    @given(text(), text())
    def test_mkdir_and_directory_exists_afterwards(self, directory: str, _file: str):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)

        assume("/" not in _file)
        assume(_file not in self.ILLEGAL_DIRECTORY_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)
        os.mkdir("/" + directory + "/" + _file)

        assert os.filesystem.has(Path("/" + directory + "/" + _file))

    @given(text())
    def test_mkdir_works(self, directory):
        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)
        os.mkdir("/" + directory)

    @given(text(), sets(text()))
    @example("0", set())
    def test_listdir_with_subdirectories_only(self, directory, subdirectories):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)
        for subdirectory in subdirectories:
            assume(subdirectory not in self.ILLEGAL_DIRECTORY_NAMES)
            assume("/" not in subdirectory)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))
        os.mkdir("/" + directory)

        for subdirectory in subdirectories:
            os.mkdir("/" + directory + "/" + subdirectory)

        assert sorted(subdirectories) == sorted(os.listdir("/" + directory))

    @given(text())
    def test_listdir_empty_directory(self, directory):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)

        os = FakeOS(
            filesystem=FakeFilesystem(directories=[FakeDirectory(Path("/"))]))

        os.mkdir("/" + directory)

        assert os.listdir("/" + directory) == []

    @given(text(), text())
    def test_listdir_with_a_file_inside(self, directory, filename):
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)
        assume("/" not in filename)
        assume(filename not in self.ILLEGAL_DIRECTORY_NAMES)

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
        assume("/" not in directory)
        assume(directory not in self.ILLEGAL_DIRECTORY_NAMES)
        assume("/" not in filename)
        assume(filename not in self.ILLEGAL_DIRECTORY_NAMES)
        assume("/" not in subdirectory)
        assume(subdirectory not in self.ILLEGAL_DIRECTORY_NAMES)

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


class CurrentDirectoryCase(TestCase):
    ILLEGAL_DIRECTORY_NAMES = ("", ".", "..")

    @given(text())
    def test_chdir(self, path):
        assume("/" not in path)
        assume(path not in self.ILLEGAL_DIRECTORY_NAMES)

        os = FakeOS()
        os.mkdir(path)
        os.chdir(path)
        assert os.getcwd() == str(Path(path).absolute())

    @given(text())
    def test_chdir_directory_does_not_exist(self, path):
        assume("/" not in path)
        assume(path not in self.ILLEGAL_DIRECTORY_NAMES)

        os = FakeOS()
        with self.assertRaises(FileNotFoundError):
            os.chdir(path)

    @given(text())
    def test_chdir_directory_path_is_a_file(self, path):
        assume("/" not in path)
        assume(path not in self.ILLEGAL_DIRECTORY_NAMES)

        os = FakeOS(filesystem=FakeFilesystem(files=[FakeFile(Path(path))]))
        with self.assertRaises(NotADirectoryError):
            os.chdir(path)