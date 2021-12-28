from uuid import uuid4, UUID

import pytest

from account.account import Account
from database.implementations.pandas_db import AccountDatabasePandas
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.ram import AccountDatabaseRAM
from database.database import ObjectNotFound


class TestRAMDatabase:
    def test_all_dbs(self) -> None:
        connection = "dbname=defaultdb port=25060 user=doadmin password=e5Y6G88wWs0EGS5e host=db-postgresql-nyc3-99638-do-user-4060406-0.b.db.ondigitalocean.com"
        all_implementations = [AccountDatabaseRAM, AccountDatabasePandas, AccountDatabasePostgres]
        for implementation in all_implementations:
            print()
            print("------------- Now testing", implementation.__name__)
            if implementation == AccountDatabasePostgres:
                database = AccountDatabasePostgres(connection=connection)
            else:
                database = implementation()
            account = Account.random()
            account2 = Account.random()
            database.save(account)
            database.save(account2)
            got_account = database.get_object(account.id_)
            assert account == got_account

            with pytest.raises(ObjectNotFound):
                database.get_object(uuid4())

            if implementation == AccountDatabaseRAM:
                all_objects = database.get_objects()
                assert len(all_objects) == 2
                for acc in all_objects:
                    assert isinstance(acc, Account)

            got_account = database.get_object(account.id_)
            assert account == got_account

    def test_all_dbs_persistent(self) -> None:
        all_implementations = [AccountDatabasePandas]

        for implementation in all_implementations:
            print()
            print("------------- Now testing persistence", implementation.__name__)
            database = implementation()
            account = Account.random()
            account2 = Account.random()
            database.save(account)
            database.save(account2)

            got_account = database.get_object(account.id_)
            assert account == got_account

            with pytest.raises(ObjectNotFound):
                database.get_object(uuid4())

            database.delete(account)

            with pytest.raises(ObjectNotFound):
                database.get_object(account)

            account_null = Account()
            with pytest.raises(ObjectNotFound):
                database.delete(account_null)

    def test_connection(self) -> None:
        connection = "dbname=defaultdb port=25060 user=doadmin password=e5Y6G88wWs0EGS5e host=db-postgresql-nyc3-99638-do-user-4060406-0.b.db.ondigitalocean.com"
        database = AccountDatabasePostgres(connection=connection)
        database.save(Account.random())
        all_accounts = database.get_objects()
        print(all_accounts)
        database.close_connection()

    def test_del_account(self) -> None:
        database = AccountDatabasePandas('E:/Kaspi lab/Part 4. Python/Day 1/kaspi_accounts/')

        account = database.get_object(id_=UUID('559de899-cda9-4401-9cfb-e8f3af8f6e62'))
        database.delete(account)