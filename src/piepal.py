import requests
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.text import Text
import datetime
import sys
import argparse
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')

API_BASE = 'https://api-m.paypal.com'
VERBOSE = False

console = Console()

def verbose_log(str):
    global VERBOSE
    if VERBOSE:
        console.log(str)

def get_access_token():
    url = f"{API_BASE}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    verbose_log(f"POST {url}")
    response.raise_for_status()
    return response.json()['access_token']


def get_nested_value(data, key_path, default="N/A"):
    if not isinstance(data, dict):
        return default

    keys = key_path.split(".")
    value = data

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, default)
        else:
            return default

    return value if value is not None else default

def render_dict_table(data, fields, title=False):
    if not all(isinstance(field, (tuple, list)) and len(field) == 3 for field in fields):
        raise ValueError("Each field must be a (key_path, label, color) tuple.")

    table = Table(title=title,  show_lines=True)
    for _, label, color in fields:
        table.add_column(label, style=color)

    for row in data:
        table.add_row(*[
            str(get_nested_value(row, key_path)) for key_path, _, _ in fields
        ])

    if data:
        console.print(table)
    else:
        console.print(f"[yellow]No data to display in '{title}'[/yellow]")

def render_vertical_table(data, fields, title="Details"):
    table = Table(title=title, show_lines=True, show_header=True, header_style="bold")
    table.add_column("Name", style="bold white")
    table.add_column("Value")

    for key_path, label, color in fields:
        for row in data:
            value = str(get_nested_value(row, key_path))
            table.add_row(label, f"[{color}]{value}[/{color}]")

    console.print(table)

def render_dict_tree(data, title="Data Tree"):
    tree = Tree(f"[bold cyan]{title}[/bold cyan]")
    build_tree(data, tree)
    console.print(tree)


def build_tree(obj, tree):
    if isinstance(obj, dict):
        for key, value in obj.items():
            branch = tree.add(f"[bold white]{key}[/bold white]")
            build_tree(value, branch)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            branch = tree.add(f"[bold green][{idx}][/bold green]")
            build_tree(item, branch)
    else:
        # Leaf node
        tree.add(Text(str(obj), style="white"))

def print_subscription_report(data, args):
    fields = (
        ("id", "Subscription ID", "purple"),
        ("plan_id", "Plan ID", "purple"),
        ("status", "Status", "green"),
        ("billing_info.last_payment.amount.value", "Amount", "green"),
        ("billing_info.last_payment.amount.currency_code", "Currency", "green"),
        ("billing_info.last_payment.time", "Last Payment Time", "cyan"),
        ("status_update_time", "Status Update Time", "cyan"),
        ("billing_info.next_billing_time", "Next Billing Time", "cyan"),
        ("start_time", "Start Time", "cyan"),
        ("update_time", "Update Time", "cyan"),
        ("billing_info.failed_payments_count", "Failed CX", "green"),
        ("subscriber.email_address", "Subscriber Email", "white"),
        ("subscriber.name", "Subscriber Name", "white"),
        ("subscriber.payer_id", "Payer ID", "purple"),
    )
    console.rule(f"[bold blue]Subscription Report {data['id']}")
    #render_dict_table([data], fields, False)
    render_vertical_table([data], fields, f"Subscription {data['id']}")
    if args.debug and args.debug == 1:
        render_dict_tree(data, title=f"Subcription {data['id']} Object Dump ")

def print_transactions_report(data, args):
    fields = (
        ("id", "Transaction ID", "purple"),
        ("status", "Status", "green"),
        ("amount_with_breakdown.gross_amount.value", "Amount Gross", "green"),
        ("amount_with_breakdown.net_amount.value", "Amount Net", "green"),
        ("amount_with_breakdown.fee_amount.value", "Fee", "green"),
        ("amount_with_breakdown.gross_amount.currency_code", "Currency", "green"),
        ("time", "Time", "cyan"),
        ("payer_email", "Payer Email", "white"),
    )
    console.rule(f"[bold blue]Transactions Report for Subscription {args.sub}")
    render_dict_table(data, fields, False)
    if args.debug and args.debug == 1:
        render_dict_tree(data, title=f"Transactions Object Dump ")


def print_transaction_details_report(data, args):
    fields = (
        ("transaction_id", "Transaction ID", "purple"),
        ("paypal_reference_id", "PayPal Reference ID", "purple"),
        ("transaction_status", "Transaction Status", "green"),
        ("transaction_event_code", "Transaction Event Code", "purple"),
        ("transaction_amount.value", "Amount", "green"),
        ("fee_amount.value", "Fee", "green"),
        ("transaction_amount.currency_code", "Amount", "green"),
        ("instrument_type", "Instrument", "white"),
        ("transaction_subject", "Transaction Subject", "white"),
        ("custom_field", "Custom", "white"),
    )
    console.rule(f"[bold blue]Transaction Details {args.txn}")
    transaction = data['transaction_info']
    render_vertical_table([transaction], fields, False)
    if args.debug and args.debug == 1:
        render_dict_tree(transaction, title=f"Transaction Details Object Dump")

def print_transactions_list_report(data, args):
    fields = (
        ("transaction_info.transaction_id", "Transaction ID", "purple"),
        ("transaction_info.paypal_reference_id", "PayPal Reference ID", "purple"),
        ("transaction_info.transaction_event_code", "Type", "purple"),
        ("transaction_info.transaction_status", "Status", "green"),
        ("transaction_info.transaction_initiation_date", "Transaction Init Date", "green"),
        ("transaction_info.transaction_amount.value", "Amount", "green"),
        ("transaction_info.fee_amount.value", "Fee", "green"),
        ("transaction_info.transaction_amount.currency_code", "Amount", "green"),
        # ("transaction_info.instrument_type", "Instrument", "white"),
        # ("transaction_info.transaction_subject", "Transaction Subject", "white"),
        # ("transaction_info.custom_field", "Custom", "white"),
    )
    console.rule(f"[bold blue]Transactions List")

    render_dict_table(data['transaction_details'], fields, False)
    if args.debug and args.debug == 1:
        render_dict_tree(transaction, title=f"Transaction Details Object Dump")



def print_plan_details_report(data, args):
    fields = (
        ("id", "Plan ID", "purple"),
        ("product_id", "Product ID", "purple"),
        ("name", "Name", "white"),
        ("status", "Status", "green"),
        ("create_time", "Create Time", "green"),
        ("update_time", "Update Time", "green"),
        ("usage_type", "Usage type", "green"),
        ("payment_preferences", "Preferences", "white"),
    )
    console.rule(f"[bold blue]Plan Details {data['id']}")
    render_vertical_table([data], fields, False)
    if args.debug and args.debug == 1:
        render_dict_tree(data, title=f"Plan Object Dump")


def get_subscription_details(token, subscription_id):
    url = f"{API_BASE}/v1/billing/subscriptions/{subscription_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    verbose_log(f"GET {url}")
    response.raise_for_status()
    return response.json()

def get_transactions_by_subscription(token, subscription_id):
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(days=60)
    current_start = start_time
    all_transactions = []

    while current_start < now:
        current_end = min(current_start + datetime.timedelta(days=31), now)
        start_str = current_start.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_str = current_end.strftime("%Y-%m-%dT%H:%M:%SZ")

        url = f"{API_BASE}/v1/billing/subscriptions/{subscription_id}/transactions"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'start_time': start_str,
            'end_time': end_str
        }

        response = requests.get(url, headers=headers, params=params)
        verbose_log(f"GET {url}")
        response.raise_for_status()
        transactions = response.json().get("transactions", [])
        all_transactions.extend(transactions)

        current_start = current_end + datetime.timedelta(seconds=1)

    return all_transactions

def get_transactions(access_token, transaction_id, start_date, end_date, txn_type=None, page=1, page_size=20):
    url = f"{API_BASE}/v1/reporting/transactions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "fields": "all",
        "page_size": str(page_size),
        "page": str(page),
        "transaction_status": "S"
    }

    if transaction_id:
        params['transaction_id'] = transaction_id

    if txn_type:
        params["transaction_type"] = txn_type

    response = requests.get(url, headers=headers, params=params)
    verbose_log(f"GET {url}")
    response.raise_for_status()
    return response.json()

def main():
    global VERBOSE
    global API_BASE
    
    parser = argparse.ArgumentParser(description="[PiePal] - PayPal API Viewer written with Python")
    parser.add_argument("--transactions", action=argparse.BooleanOptionalAction, help="List latest transactions")
    parser.add_argument("--sub", help="Subscription ID to fetch details")
    parser.add_argument("--txn", help="Transaction ID to fetch details")
    parser.add_argument("--plan", help="Plan ID to fetch")
    parser.add_argument("--sandbox", action=argparse.BooleanOptionalAction, help="Use SANDBOX environment")
    parser.add_argument("--debug", action=argparse.BooleanOptionalAction, help="Debug output")
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, help="Verbose output")

    with console.status("Doing job...", spinner="dots"):
        try:
            args = parser.parse_args()
            console.print()
            console.print("--== PiePAL - PayPal observability tool ==-- (run -h to get more information)", justify="center")
            console.print()

            if args.sandbox:
                API_BASE='https://api-m.sandbox.paypal.com'
            else:
                API_BASE='https://api-m.paypal.com'

            if args.verbose:
                VERBOSE=True
            else:
                VERBOSE=False

            if args.sub:
                token = get_access_token()
                subscription_data = get_subscription_details(token, args.sub)
                subscription_transactions_data = get_transactions_by_subscription(token, args.sub)
                print_subscription_report(subscription_data, args)
                print_transactions_report(subscription_transactions_data, args)
            if args.txn:
                token = get_access_token()
                end = datetime.datetime.utcnow()
                start = end - datetime.timedelta(days=2)
                start_str = start.strftime('%Y-%m-%dT%H:%M:%SZ')
                end_str = end.strftime('%Y-%m-%dT%H:%M:%SZ')

                data = get_transactions(
                    token,
                    False,
                    start_str,
                    end_str,
                    txn_type=None,
                    page=1,
                    page_size=20
                )
                print_transaction_details_report(data['transaction_details'][0], args)
            if args.transactions:
                token = get_access_token()
                end = datetime.datetime.utcnow()
                start = end - datetime.timedelta(days=2)
                start_str = start.strftime('%Y-%m-%dT%H:%M:%SZ')
                end_str = end.strftime('%Y-%m-%dT%H:%M:%SZ')

                data = get_transactions(
                    token,
                    False,
                    start_str,
                    end_str,
                    txn_type=None,
                    page=1,
                    page_size=20
                )
                print_transactions_list_report(data, args)
            if args.plan:
                print_plan_details_report(plan_data, args)

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)
    return
