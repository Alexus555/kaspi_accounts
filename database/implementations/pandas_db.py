import datetime
import uuid
from typing import List
from uuid import UUID, uuid4
import pandas as pd
from pandas import DataFrame
from account.account import Account
from account.account_data import AccountData
from balance_history.balance_history import BalanceHistory
from transaction.transaction import Transaction
from customer.customer import Customer
from database.database import AccountDatabase
from database.database import CustomerDatabase
from database.database import TransactionDatabase
from database.database import ObjectNotFound


class AccountDatabasePandas(AccountDatabase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects: DataFrame = pd.DataFrame(columns=["id", "currency", "balance", "customer_id"])
        try:
            self._objects = pd.read_pickle("account_db.pk")
            print("Got database from disk:", self._objects)
        except:
            pass

    def save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()

        if account.id_ in list(self._objects["id"]):
            self._objects = self._objects[self._objects["id"] != account.id_]

        new_row = pd.DataFrame({
            "id": [account.id_],
            "currency": [account.currency],
            "balance": [account.balance],
            "customer_id": [account.customer_id],
        })
        self._objects = self._objects.append(new_row)
        self._objects.to_pickle("account_db.pk")

        print('Account {} saved'.format(account))

    def get_objects(self) -> List[Account]:
        result = []
        for index, row in self._objects.iterrows():
            result.append(Account(
                id_=row["id"],
                currency=row["currency"],
                balance=row["balance"],
                customer_id=row["customer_id"],
            ))

        return result

    def get_objects_views(self) -> List[AccountData]:
        result = []
        for index, row in self._objects.iterrows():
            result.append(
                AccountData(
                account=Account(
                        id_=row["id"],
                        currency=row["currency"],
                        balance=row["balance"],
                        customer_id=row["customer_id"],
                        ),
                customer=CustomerDatabasePandas().get_object(row["customer_id"]))
                )

        return result

    def get_objects_by_customer(self, customer_id: UUID) -> List[Account]:
        result = []
        for index, row in self._objects.loc[self._objects['customer_id'] == customer_id].iterrows():
            result.append(Account(
                id_=row["id"],
                currency=row["currency"],
                balance=row["balance"],
                customer_id=row["customer_id"]
            ))
        return result

    def get_object(self, id_: UUID) -> Account:
        if id_ in list(self._objects["id"]):
            filtered = self._objects[self._objects["id"] == id_].iloc[0]
            account = Account(
                id_=filtered["id"],
                currency=filtered["currency"],
                balance=filtered["balance"],
                customer_id=filtered["customer_id"]
            )
            return account
        print("--------this object is not found:", id_)
        print(self._objects.info())
        raise ObjectNotFound("Pandas error: object not found")

    def delete(self, account: Account) -> None:
        if account.id_ is None:
            raise ObjectNotFound("Pandas error: object is null")

        if account.id_ not in list(self._objects["id"]):
            raise ObjectNotFound("Pandas error: object not found")

        self._objects.set_index('id')
        self._objects.drop([account.id_], axis=0, inplace=True)
        self._objects.to_pickle("account_db.pk")


class CustomerDatabasePandas(CustomerDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects: DataFrame = pd.DataFrame(columns=["id", "age", "first_name", "last_name"])
        try:
            self._objects = pd.read_pickle("customer_db.pk")
            print("Got database from disk:", self._objects)
        except:
            pass

    def save(self, customer: Customer) -> None:
        if customer.id_ is None:
            customer.id_ = uuid4()

        if customer.id_ in list(self._objects["id"]):
            self._objects = self._objects[self._objects["id"] != customer.id_]

        new_row = pd.DataFrame({
            "id": [customer.id_],
            "age": [customer.age],
            "first_name": [customer.first_name],
            "last_name": [customer.last_name],
        })
        self._objects = self._objects.append(new_row)
        self._objects.to_pickle("customer_db.pk")

    def get_objects(self) -> List[Customer]:
        result = []
        for index, row in self._objects.sort_values(by=['first_name', 'last_name']).iterrows():
            result.append(Customer(
                id_=row["id"],
                age=row["age"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                accounts=AccountDatabasePandas().get_objects_by_customer(customer_id=row["id"])
            ))
        return result

    def get_object(self, id_: UUID) -> Customer:
        if id_ in list(self._objects["id"]):
            filtered = self._objects[self._objects["id"] == id_].iloc[0]
            customer = Customer(
                id_=filtered["id"],
                age=filtered["age"],
                first_name=filtered["first_name"],
                last_name=filtered["last_name"],
                accounts=AccountDatabasePandas().get_objects_by_customer(customer_id=filtered["id"])
            )
            return customer
        print("--------this object is not found:", id_)
        print(self._objects.info())
        raise ObjectNotFound("Pandas error: object not found")

    def delete(self, customer: Customer) -> None:
        if customer.id_ is None:
            raise ObjectNotFound("Pandas error: object is null")

        if customer.id_ not in list(self._objects["id"]):
            raise ObjectNotFound("Pandas error: object not found")

        self._objects.set_index('id')
        self._objects.drop([customer.id_], axis=0, inplace=True)
        self._objects.to_pickle("customer_db.pk")


class TransactionDatabasePandas(TransactionDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects: DataFrame = \
            pd.DataFrame(
                columns=[
                    "id",
                    "date",
                    "sender_account_id",
                    "recipient_account_id",
                    "sender_customer_id",
                    "recipient_customer_id",
                    "amount",
                    "currency",
                    "type",
                ])
        try:
            self._objects = pd.read_pickle("transaction_db.pk")
            print("Got database from disk:", self._objects)
        except:
            pass

    def save(self, transaction: Transaction) -> None:
        if transaction.id_ is None:
            transaction.id_ = uuid4()

        if transaction.id_ in list(self._objects["id"]):
            self._objects = self._objects[self._objects["id"] != transaction.id_]

        new_row = pd.DataFrame({
            "id": [transaction.id_],
            "date": [transaction.date],
            "sender_account_id": [transaction.sender_account_id],
            "recipient_account_id": [transaction.recipient_account_id],
            "amount": [transaction.amount],
            "currency": [transaction.currency],
            "type": [transaction.type],
        })
        self._objects = self._objects.append(new_row)
        self._objects.to_pickle("transaction_db.pk")

        print('Transaction {} saved'.format(transaction))



    def get_objects(self) -> List[Transaction]:
        result = []
        transactions = self._objects
        for index, row in transactions.sort_values(by=['date']).iterrows():
            result.append(Transaction(
                id_=row["id"],
                date=row["date"],
                sender_account_id=row["sender_account_id"],
                recipient_account_id=row["recipient_account_id"],
                amount=row["amount"],
                currency=row["currency"],
                type=row["type"],
            ))
        return result

    def get_object(self, id_: UUID) -> Transaction:
        if id_ in list(self._objects["id"]):
            filtered = self._objects[self._objects["id"] == id_].iloc[0]
            account = Transaction(
                id_=filtered["id"],
                date=filtered["date"],
                sender_account_id=filtered["sender_account_id"],
                recipient_account_id=filtered["recipient_account_id"],
                amount=filtered["amount"],
                currency=filtered["currency"],
                type=filtered["type"],
            )
            return account
        print("--------this object is not found:", id_)
        print(self._objects.info())
        raise ObjectNotFound("Pandas error: object not found")

    def get_objects_by_account(self, account_id: UUID) -> List[Transaction]:
        result = []
        transactions = self._objects
        for index, row in transactions.sort_values(by=['date']).iterrows():
            if row["sender_account_id"] != account_id \
                    and row["recipient_account_id"] != account_id:
                continue
            result.append(Transaction(
                id_=row["id"],
                date=row["date"],
                sender_account_id=row["sender_account_id"],
                recipient_account_id=row["recipient_account_id"],
                amount=row["amount"],
                currency=row["currency"],
                type=row["type"],
            ))
        return result

    def get_balance_history_by_account(self, account_id: UUID) -> List[BalanceHistory]:
        result = {'2021-01-01': 0}
        balance = 0

        if account_id is not None:
            str_account_id = str(account_id)
            transactions = self._objects
            # .loc[
            #     str(self._objects['sender_account_id']) == str_account_id
            #     | str(self._objects['recipient_account_id']) == str_account_id
            # ]
            print('Calcalating balance history...')

            for index, row in transactions.sort_values(by=['date']).iterrows():
                if row["sender_account_id"] != account_id \
                        and row["recipient_account_id"] != account_id:
                    continue

                if row["sender_account_id"] == row["recipient_account_id"]:
                    delta = row["amount"]
                elif row["sender_account_id"] == account_id:
                    delta = -row["amount"]
                else:
                    delta = row["amount"]

                balance += delta

                date = row["date"].strftime('%Y-%m-%d')

                print(date, balance)

                if result.get(date) is None:
                    result[date] = 0

                result[date] += balance

        date = datetime.datetime.now().strftime('%Y-%m-%d')

        if result.get(date) is None:
            result[date] = balance

        balance_history = []
        for key in result:
            balance_history.append(BalanceHistory(key, result[key]))

        return balance_history

    def delete(self, transaction: Transaction) -> None:
        if transaction.id_ is None:
            raise ObjectNotFound("Pandas error: object is null")

        if transaction.id_ not in list(self._objects["id"]):
            raise ObjectNotFound("Pandas error: object not found")

        self._objects.set_index('id')
        self._objects.drop([transaction.id_], axis=0, inplace=True)
        self._objects.to_pickle("transaction_db.pk")


class DatabaseManagerPandas:
    accounts: AccountDatabasePandas
    customers: CustomerDatabasePandas
    transactions: TransactionDatabasePandas

    def __init__(self):
        self.accounts = AccountDatabasePandas()
        self.customers = CustomerDatabasePandas()
        self.transactions = TransactionDatabasePandas()
