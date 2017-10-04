from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from fakeos import FakeOS, FakeEnvironment

class EnvironmentTest(TestCase):
    @given(text())
    def test_environ_getting_non_existing_variable(self, variable):
        os = FakeOS()

        assert os.environ()[variable] == str()

    @given(text(), text())
    def test_environ_getting_existing_variable(self, variable, value):
        os = FakeOS(environment=FakeEnvironment({variable: value}))

        assert os.environ()[variable] == value
