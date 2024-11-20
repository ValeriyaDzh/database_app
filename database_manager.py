from typing import Any

from database import Database, Transaction


class DatabaseManager:

    db: Database = Database()
    transactions: list[Transaction] = []

    @classmethod
    def apply_to_active_transaction_or_db(cls, method_name: str, *args: Any) -> None:
        if cls.transactions:
            getattr(cls.transactions[-1], method_name)(*args)
        else:
            getattr(cls.db, method_name)(*args)

    @classmethod
    def get_from_active_transaction_or_db(cls, method_name: str, *args: Any) -> Any:
        if cls.transactions:
            return getattr(cls.transactions[-1], method_name)(*args)
        return getattr(cls.db, method_name)(*args)

    @classmethod
    def begin_transaction(cls) -> None:
        snapshot = (
            cls.transactions[-1].rollback() if cls.transactions else cls.db.copy()
        )
        cls.transactions.append(Transaction(snapshot))

    @classmethod
    def rollback_transaction(cls) -> None:
        if cls._is_transactions_exist():
            cls.transactions.pop()

    @classmethod
    def commit_transaction(cls) -> None:
        if cls._is_transactions_exist():
            transaction = cls.transactions.pop()
            transaction.commit(cls.db)

    @classmethod
    def _is_transactions_exist(cls) -> bool:
        return cls.transactions if cls.transactions else print("NO TRANSACTION")
