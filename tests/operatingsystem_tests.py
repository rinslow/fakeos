from unittest import TestCase

from fakeos import FakeOS
from operating_system import FakeWindows, FakeUnix


class OSStatsCase(TestCase):
    def test_cpu_count(self):
        os = FakeOS(operating_system=FakeUnix(cpu_count=2))

        assert os.cpu_count() == 2

    def test_uname_on_unix(self):
        os = FakeOS(operating_system=FakeUnix(sysname="a",
                                              nodename="b",
                                              release="c",
                                              version="d",
                                              machine="e"))

        assert list(os.uname()) == list("abcde")

    def test_uname_on_windows(self):
        os = FakeOS(operating_system=FakeWindows())

        with self.assertRaises(AttributeError):
            os.uname()