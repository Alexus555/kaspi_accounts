from dataclasses import dataclass
from typing import List
from uuid import UUID, uuid4

from account.account import Account


@dataclass
class Customer:
    id_: UUID
    age: int
    first_name: str
    last_name: str
    accounts: List[Account]

    # def __init__(self, _id, age, first_name, last_name, accounts=[]):
    #     self.accounts = accounts
    #     self.id_ = _id
    #     self.age = age
    #     self.first_name = first_name
    #     self.last_name = last_name

    def __lt__(self, other) -> bool:
        return self.age < other.age or self.last_name < other.last_name or self.first_name <= other.first_name

