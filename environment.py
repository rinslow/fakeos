"""Everything needed for being able to create a virtual environment."""
from collections import defaultdict


class FakeEnvironment(object):
    """I mock a computer environment."""
    def __init__(self, keys: dict=None):
        self.keys = keys or dict()

    def __getitem__(self, item):
        return self.keys.get(item, str())

    def __iter__(self):
        return self.keys.items()

    def __len__(self):
        return len(self.keys)

    def environ(self) -> defaultdict:
        return defaultdict(str, self.keys)
