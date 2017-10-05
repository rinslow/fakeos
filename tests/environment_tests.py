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
        os = FakeOS(environment=FakeEnvironment(keys={variable: value}))

        assert os.environ()[variable] == value

    @given(text(), text())
    def test_get_env_when_variable_does_not_exist(self, variable, default):
        os = FakeOS()

        assert os.getenv(variable, default) == default

    @given(text(), text())
    def test_get_env_when_variable_exists(self, variable, value):
        os = FakeOS(environment=FakeEnvironment(keys={variable: value}))

        assert os.getenv(variable) == value

    @given(text(), text())
    def test_putenv_and_then_getenv(self, variable, value):
        os = FakeOS()
        os.putenv(variable, value)

        assert os.getenv(variable) == value
