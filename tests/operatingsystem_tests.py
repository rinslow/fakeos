from unittest import TestCase

from fakeos import FakeOS, FakeUnix


class OSStatsCase(TestCase):
    def test_cpu_count(self):
        os = FakeOS(operating_system=FakeUnix(cpu_count=2))

        assert os.cpu_count() == 2