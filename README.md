# PiePAL - Terminal Tool for PayPal Observability

A Python program to fetch and display PayPal transactions and subscription details. The script uses the PayPal REST API to retrieve transactions related to a specific **Subscription ID** and can display them in a terminal using the **`rich`** library for a formatted and clean output.

## Features

- Fetch **Subscription** details
- Fetch **all transactions** for a given **subscription ID**.
- Display transaction details such as **Transaction ID**, **Amount**, **Payer Email**, and **Payer Name**.
- Fetch **Subscription Plan** details
- Use the **PayPal Sandbox API** for testing by using `--sandbox`
- Use `--verbose` output to understand API calls

## Setup for usage

* Install with pip - `pip install piepal`
* Set env variables 
  * `export PAYPAL_CLIENT_ID="..."`
  * `export PAYPAL_CLIENT_SECRET="..."`
* Run `piepal`

## Setup for development

* Git clone repository
* cd ./src
* Setup credentials with env variables
  * `export PAYPAL_CLIENT_ID="..."`
  * `export PAYPAL_CLIENT_SECRET="..."`


## Options

``` sh
usage: piepal [-h] [--transactions | --no-transactions] [--sub SUB] [--txn TXN] [--plan PLAN] [--sandbox | --no-sandbox] [--debug | --no-debug]
              [--verbose | --no-verbose]

[PyPal] - PayPal API Viewer written with Python

options:
  -h, --help            show this help message and exit
  --transactions, --no-transactions
                        List latest transactions
  --sub SUB             Subscription ID to fetch details
  --txn TXN             Transaction ID to fetch details
  --plan PLAN           Plan ID to fetch
  --sandbox, --no-sandbox
                        Use SANDBOX environment
  --debug, --no-debug   Debug output
  --verbose, --no-verbose
                        Verbose output
```

## Examples

### Get latest subscriptions

`piepal --transactions`

### Get Subscription details

`piepal --sub I-1234567890GG`

### Get Transaction details

`piepal --txn T-12345678990F3FG1231`

### Get Subscription Plan details

`piepal --plan P-12345678990F3FG1231`


```
                           Subscription I-1234567890GG
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name               ┃ Value                                                     ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Subscription ID    │ I-1234567890GG                                            │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Plan ID            │ P-1234567890GG123456789YYA                                │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Status             │ CANCELLED                                                 │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Amount             │ 12.5                                                      │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Currency           │ USD                                                       │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Last Payment Time  │ 2025-04-24T00:00:00Z                                      │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Status Update Time │ 2025-04-25T00:00:00Z                                      │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Next Billing Time  │ N/A                                                       │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Start Time         │ 2025-05-01T00:00:00Z                                      │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Update Time        │ 2025-04-25T00:00:00Z                                      │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Failed CX          │ 0                                                         │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Subscriber Email   │ user_email@example.com                                    │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Subscriber Name    │ {'given_name': 'John', 'surname': Snow'}                  │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Payer ID           │ DB1234567890                                              │
└────────────────────┴───────────────────────────────────────────────────────────┘

Transactions for this Subscription

+-----------------------+-------------------------+--------+----------+-------------------+----------------------+
| Transaction ID        |  Date                   | Amount | Currency | Payer Email       | Payer Name           | 
+-----------------------+-------------------------+--------+----------+-------------------+----------------------+
| 5A6789ABC1234567X     | 2025-03-31T12:00:00Z    | $50.00 | USD      | user@example.com  | John Doe             |
+-----------------------+-------------------------+--------+----------+-------------------+----------------------+
| 5A6789ABC1234567Y     | 2025-04-01T10:30:00Z    | $50.00 | USD      | user@example.com  | John Doe             |
+-----------------------+-------------------------+--------+----------+-------------------+----------------------+
```
### Screenshots

![](/screenshots/TransactionsList.jpeg)
![](/screenshots/TransactionDetails.jpeg)
![](/screenshots/SubscriptionTransactionList.jpeg)
![](/screenshots/SubscriptionReportDetails.jpeg)

## License

* MIT License  
