from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from account.account import Account
from customer.customer import Customer
from transaction.transaction import Transaction


class TestTransaction:

    def test_transaction_create(self) -> None:
        account_sender = Account.random()
        account_recipient = Account.random()

        customer_sender = Customer(
            id_=uuid4(),
            first_name='Customer',
            last_name='Sender',
            age=40,
            accounts=[account_sender]
        )

        customer_recipient = Customer(
            id_=uuid4(),
            first_name='Customer',
            last_name='Recipient',
            age=40,
            accounts=[account_recipient]
        )

        current_timestamp = datetime.now().timestamp()
        transaction_id = uuid4()
        transaction = Transaction(
            id_=transaction_id,
            account_sender=account_sender,
            account_recipient=account_recipient,
            customer_sender=customer_sender,
            customer_recipient=customer_recipient,
            timestamp=current_timestamp,
            amount=Decimal(10),
        )

        assert isinstance(transaction, Transaction)

        assert transaction.id_ == transaction_id
        assert transaction.account_sender == account_sender
        assert transaction.account_recipient == account_recipient
        assert transaction.customer_sender == customer_sender
        assert transaction.customer_recipient == customer_recipient
        assert transaction.amount == Decimal(10)
        assert transaction.timestamp == current_timestamp

        assert transaction.account_sender in customer_sender.accounts
        assert transaction.account_recipient in customer_recipient.accounts
