from dataclasses import dataclass
from decimal import Decimal

@dataclass
class BalanceHistory:
    date: str
    balance: Decimal