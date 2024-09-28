import threading


class InMemoryDB:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.matches = {}

    def __setitem__(self, key, value) -> None:
        with self.lock:
            self.matches[key] = value

    def __getitem__(self, key):
        with self.lock:
            return self.matches[key]

    def __delitem__(self, key):
        with self.lock:
            del self.matches[key]

    def get(self, key):
        with self.lock:
            return self.matches.get(key)

    def keys(self):
        with self.lock:
            return self.matches.keys()

    def values(self):
        with self.lock:
            return self.matches.values()

    def items(self):
        with self.lock:
            return self.matches.items()
