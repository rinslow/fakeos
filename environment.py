"""Everything needed for being able to create a virtual environment."""
from collections import defaultdict


class FakeEnvironment(object):
    """I mock a computer environment."""

    def __init__(self, keys: dict = None, default=None):
        self.keys = keys or dict()
        self.default = default or str()

    def __getitem__(self, item):
        return self.keys.get(item, self.default)

    def __iter__(self):
        return self.keys.items()

    def __len__(self):
        return len(self.keys)

    def environ(self) -> defaultdict:
        """Return a default-dict representing the environment."""
        return defaultdict(lambda: self.default, self.keys)

    def getenv(self, key: str, default: object = None) -> str:
        """Return environment variable if it exists, otherwise return
        default."""
        return self.keys.get(key, default)

    def putenv(self, key: str, value: str):
        """Add an environment variable."""
        self.keys[key] = value
