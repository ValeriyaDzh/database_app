from collections import deque
from copy import deepcopy


class Database:

    def __init__(self):
        self.db = {}
        self.counter_values = {}

    def get_value(self, key: str) -> int | str:
        return self.db.get(key, "NULL")

    def set_value(self, key: str, value: int) -> None:
        old_value = self.db.get(key)
        if old_value:
            self.db[key] = old_value + value
            self._reduce_counter(old_value)
        else:
            self.counter_values[value] = self.counter_values.get(value, 0) + 1
            self.db[key] = value

    def unset_value(self, key: str) -> None:
        if key in self.db:
            deleted_value = self.db.pop(key)
            self._reduce_counter(deleted_value)

    def get_keys(self, value: int) -> str:
        return " ".join(key for key, db_value in self.db.items() if db_value == value)

    def get_counter(self, key: int) -> str:
        return self.counter_values.get(key, 0)

    def _reduce_counter(self, key: int) -> None:
        self.counter_values[key] = self.counter_values.get(key, 2) - 1
        if self.counter_values[key] == 0:
            del self.counter_values[key]

    def copy(self):
        return deepcopy(self)


class Transaction:

    def __init__(self, database: "Database"):
        self.db_snapshot = database
        self.methods = deque()

    def get_value(self, key: str) -> int | str:
        return self.db_snapshot.get_value(key)

    def set_value(self, key: str, value: int) -> None:
        self.methods.append(("set_value", key, value))
        return self.db_snapshot.set_value(key, value)

    def unset_value(self, key: str) -> None:
        self.methods.append(("unset_value", key))
        return self.db_snapshot.unset_value(key)

    def get_keys(self, value: int) -> str:
        return self.db_snapshot.get_keys(value)

    def get_counter(self, key: int) -> int:
        return self.db_snapshot.get_counter(key)

    def commit(self, db: "Database") -> None:
        while self.methods:
            method, *args = self.methods.popleft()
            getattr(db, method)(*args)

    def rollback(self):
        return self.db_snapshot.copy()
