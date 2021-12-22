from typing import List
from uuid import UUID, uuid4
import psycopg2
import pandas as pd
from pandas import DataFrame
from account.account import Account
from database.database import AccountDatabase
from database.database import ObjectNotFound


class AccountDatabasePostgres(AccountDatabase):
    def __init__(self, connection: str,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = psycopg2.connect(connection)
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id varchar primary key ,
            currency varchar ,
            balance decimal 
        );
        """)
        self.conn.commit()


    def close_connection(self):
        self.conn.close()

    def save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()

        cur = self.conn.cursor()
        cur.execute("""
                INSERT INTO accounts (id, currency, balance) VALUES (%s, %s, %s);
                """, (str(account.id_), account.currency, account.balance))
        self.conn.commit()

    def get_objects(self) -> List[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts;")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return df

    def get_object(self, id_: UUID) -> Account:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE id=%s;", str(id_))
        data = cur.fetchone()
        if data:
            account = Account(
                id_=data["id"],
                currency=data["currency"],
                balance=data["balance"],
            )
            return account

        raise ObjectNotFound("Postgres error: object not found")

    def delete(self, account: Account) -> None:
        if account.id_ is None:
            raise ObjectNotFound("Postgres error: object is null")

        cur = self.conn.cursor()
        cur.execute("""
                        DELETE accounts WHERE id=%s;
                        """, str(account.id_))
        self.conn.commit()

