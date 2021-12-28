from account.account import Account
from customer.customer import Customer


class AccountData:
    account: Account
    customer: Customer

    def __init__(self, account, customer):
        self.account = account
        self.customer = customer