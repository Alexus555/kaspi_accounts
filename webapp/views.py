import datetime
import json
from decimal import Decimal
from uuid import uuid4
import uuid

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
import os

from django.shortcuts import render

from account.account import Account
from customer.customer import Customer
from database.database import ObjectNotFound
from database.implementations.pandas_db import DatabaseManagerPandas
from transaction.transaction import Transaction

database = DatabaseManagerPandas()

def accounts_list(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        accounts = database.accounts.get_objects()
        return render(request, "accounts.html", context={"accounts": accounts})

def account(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        id_ = request.GET.get("id", None)
        print(id_)
        if id_ is None:
            account = None
            customer_full_name = 'No one'
        else:
            id_ = uuid.UUID(id_)
            account = database.accounts.get_object(id_)
            customer = database.customers.get_object(account.customer_id)
            customer_full_name = " ".join([customer.first_name, customer.last_name])

        currencies = ["KZT", "USD", "EUR"]
        customers = database.customers.get_objects()
        balance_history = database.transactions.get_balance_history_by_account(id_)
        transactions = database.transactions.get_objects_by_account(id_)

        return render(
            request, "account.html",
            context={
                "account": account,
                "currencies": currencies,
                "customers": customers,
                "customer_full_name": customer_full_name,
                "balance_history": balance_history,
                "transactions": transactions
            })

    if request.method == "POST":

        account = Account(
            id_=uuid4(),
            currency=request.POST.get("account_currency"),
            customer_id=uuid.UUID(request.POST.get("account_customer")),
            balance=0,
        )

        database.accounts.save(account)

        response = redirect('/account/?id={}'.format(account.id_))
        return response


def customers_list(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        customers = database.customers.get_objects()
        return render(request, "customers.html", context={"customers": customers})


def customer(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        id_ = request.GET.get("id", None)
        print(id_)
        if id_ is None:
            customer = \
                Customer(
                    id_=None,
                    age=0,
                    first_name='',
                    last_name='',
                    accounts=[],
                )
        else:
            customer = database.customers.get_object(uuid.UUID(id_))
        return render(request, "customer.html", context={"customer": customer})

    if request.method == "POST":
        id_ = request.POST.get("customer_id", 'None')
        print(id_)

        if id_ == 'None':
            id_ = uuid4()
        else:
            id_ = uuid.UUID(id_)

        customer = Customer(
            id_=id_,
            first_name=request.POST.get("customer_first_name"),
            last_name=request.POST.get("customer_last_name"),
            age=request.POST.get("customer_age"),
            accounts=[],
        )

        database.customers.save(customer)

        response = redirect('/customer/?id={}'.format(customer.id_))
        return response

def transactions_list(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        transactions = database.transactions.get_objects()
        return render(request, "transactions.html", context={"transactions": transactions})

def transaction(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        id_ = request.GET.get("id", 'None')
        message = request.GET.get("message", '')
        print(id_)
        if id_ == 'None':
            transaction = None
        else:
            transaction = database.transactions.get_object(uuid.UUID(id_))

        currencies = ["KZT", "USD", "EUR"]
        transaction_types = ["Add", "Send", "Withdrew"]
        accounts = database.accounts.get_objects_views()


        return render(
            request, "transaction.html",
            context={
                "transaction": transaction,
                "transaction_types": transaction_types,
                "currencies": currencies,
                "accounts": accounts,
                "message": message
            })

    if request.method == "POST":
        message = ''
        transaction_datetime = ' '.join(
                    [
                        request.POST.get("transaction_date"),
                        request.POST.get("transaction_time"),
                    ])

        print(transaction_datetime)

        transaction = Transaction(
            id_=None,
            date=datetime.datetime.strptime(transaction_datetime, '%Y-%m-%d %H:%M'),
            currency=request.POST.get("transaction_currency"),
            type=request.POST.get("transaction_type"),
            sender_account_id=uuid.UUID(request.POST.get("transaction_sender_account")),
            recipient_account_id=uuid.UUID(request.POST.get("transaction_recipient_account")),
            amount=Decimal(request.POST.get("transaction_amount")),
        )

        print('Process transaction: {}'.format(transaction))

        try:

            account_db = database.accounts

            if transaction.type == 'Withdrew' or transaction.type == 'Send':
                account = account_db.get_object(transaction.sender_account_id)
                if account.balance < transaction.amount:
                    raise ValueError('Not enough balance')

            if transaction.type == 'Add':
                transaction.sender_account_id = None

            if transaction.type == 'Withdrew':
                transaction.recipient_account_id = None

            database.transactions.save(transaction)

            if transaction.type == 'Add' or transaction.type == 'Send':
                account = account_db.get_object(transaction.recipient_account_id)
                account.balance += transaction.amount
                account_db.save(account)

            if transaction.type == 'Withdrew' or transaction.type == 'Send':
                account = account_db.get_object(transaction.sender_account_id)
                account.balance -= transaction.amount
                account_db.save(account)

        except Exception as e:
             message = str(e)

        if message == '':
            response = redirect('/transactions/')
        else:
            transaction.id_ = None
            response = redirect('/transaction/?id={}&message={}'.format(transaction.id_, message))
        return response

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")
