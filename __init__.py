"""Full mock of the builtin 'os' module for blazing-fast unit-testing."""
# pylint: disable=import-self
from fakeos import FakeOS
from filesystem import FakeFilesystem, FakeDirectory, FakeFile
