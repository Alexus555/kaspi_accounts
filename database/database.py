from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from account.account import Account
from customer.customer import Customer
from transaction.transaction import Transaction


class ObjectNotFound(ValueError):
    ...


@dataclass
class AccountDatabase(ABC):
    @abstractmethod
    def save(self, account: Account) -> None:
        ...

    @abstractmethod
    def get_objects(self) -> List[Account]:
        ...

    @abstractmethod
    def get_objects_by_customer(self, customer_id: int) -> List[Account]:
        ...

    @abstractmethod
    def get_object(self, id_: int) -> Account:
        ...

    @abstractmethod
    def delete(self, account: Account) -> None:
        ...

@dataclass
class CustomerDatabase(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> None:
        ...

    @abstractmethod
    def get_objects(self) -> List[Customer]:
        ...

    @abstractmethod
    def get_object(self, id_: int) -> Customer:
        ...

    @abstractmethod
    def delete(self, customer: Customer) -> None:
        ...

@dataclass
class TransactionDatabase(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> None:
        ...

    @abstractmethod
    def get_objects(self) -> List[Transaction]:
        ...

    @abstractmethod
    def get_objects_by_account(self, account_id: int) -> List[Transaction]:
        ...

    @abstractmethod
    def get_object(self, id_: int) -> Transaction:
        ...

    @abstractmethod
    def delete(self, transaction: Transaction) -> None:
        ...

