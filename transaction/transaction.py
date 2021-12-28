import datetime
from decimal import Decimal
from uuid import uuid4, UUID
from dataclasses import dataclass
from account.account import Account
from customer.customer import Customer


@dataclass
class Transaction:
    id_: UUID
    date: datetime
    sender_account_id: UUID
    recipient_account_id: UUID
    amount: Decimal
    currency: str
    type: str

