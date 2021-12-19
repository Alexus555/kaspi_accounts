import datetime
from decimal import Decimal
from uuid import uuid4, UUID
from dataclasses import dataclass
from account.account import Account
from customer.customer import Customer


@dataclass
class Transaction:
    id_: UUID
    timestamp: float
    account_sender: Account
    account_recipient: Account
    customer_sender: Customer
    customer_recipient: Customer
    amount: Decimal

