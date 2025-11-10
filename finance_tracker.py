#!/usr/bin/env python3
"""
Personal Finance Tracker (Python Version)
-----------------------------------------
Features:
- Add Income / Expense transactions
- Monthly and All-time reports
- Uses OOP with dataclasses and CLI
"""

from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
from typing import List, Dict


# ------------------ Utility ------------------

def input_prompt(prompt: str) -> str:
    """Get input from user and strip whitespace."""
    return input(prompt).strip()


def parse_date(date_str: str) -> datetime:
    """Parse and validate date in DD-MM-YYYY format."""
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Invalid date format. Use DD-MM-YYYY.")


def month_year_key(date: datetime) -> str:
    """Return 'MM-YYYY' string for a given date."""
    return date.strftime("%m-%Y")


# ------------------ Transaction Classes ------------------

@dataclass
class Transaction:
    amount: float
    category: str
    date: datetime
    description: str = ""

    def apply(self, account: "Account") -> None:
        """Override in subclasses."""
        raise NotImplementedError


@dataclass
class Income(Transaction):
    def apply(self, account: "Account") -> None:
        account.balance += self.amount


@dataclass
class Expense(Transaction):
    def apply(self, account: "Account") -> None:
        account.balance -= self.amount


# ------------------ Account ------------------

@dataclass
class Account:
    balance: float = 0.0
    transactions: List[Transaction] = None

    def __post_init__(self):
        if self.transactions is None:
            self.transactions = []

    def add(self, tx: Transaction) -> None:
        """Add a transaction to the account."""
        if tx.amount <= 0:
            raise ValueError("Amount must be positive.")
        tx.apply(self)
        self.transactions.append(tx)

    def by_month(self, month_year: str) -> List[Transaction]:
        """Return all transactions for a specific month-year (MM-YYYY)."""
        return [t for t in self.transactions if month_year_key(t.date) == month_year]


# ------------------ Report ------------------

@dataclass
class Report:
    total_income: float = 0.0
    total_expense: float = 0.0
    net: float = 0.0
    income_by_cat: Dict[str, float] = None
    expense_by_cat: Dict[str, float] = None

    def __post_init__(self):
        self.income_by_cat = {}
        self.expense_by_cat = {}


class ReportGenerator:
    """Handles report generation and display."""

    @staticmethod
    def monthly(account: Account, month_year: str) -> Report:
        report = Report()
        for tx in account.by_month(month_year):
            if isinstance(tx, Income):
                report.total_income += tx.amount
                report.income_by_cat[tx.category] = report.income_by_cat.get(tx.category, 0) + tx.amount
            elif isinstance(tx, Expense):
                report.total_expense += tx.amount
                report.expense_by_cat[tx.category] = report.expense_by_cat.get(tx.category, 0) + tx.amount
        report.net = report.total_income - report.total_expense
        return report

    @staticmethod
    def print_monthly(account: Account, month_year: str) -> None:
        """Print a formatted monthly report."""
        r = ReportGenerator.monthly(account, month_year)
        print(f"\n===== Monthly Report ({month_year}) =====")
        print(f"Total Income : {r.total_income:.2f}")
        print(f"Total Expense: {r.total_expense:.2f}")
        print(f"Net Savings  : {r.net:.2f}")

        print("\n-- Income by Category --")
        if r.income_by_cat:
            for cat, amt in sorted(r.income_by_cat.items()):
                print(f"  {cat}: {amt:.2f}")
        else:
            print("  None")

        print("\n-- Expense by Category --")
        if r.expense_by_cat:
            for cat, amt in sorted(r.expense_by_cat.items()):
                print(f"  {cat}: {amt:.2f}")
        else:
            print("  None")

        print("============================")
        print(f"Current Balance: Rs.{account.balance:.2f}")

    @staticmethod
    def print_all_time(account: Account) -> None:
        """Print overall financial summary."""
        income = sum(t.amount for t in account.transactions if isinstance(t, Income))
        expense = sum(t.amount for t in account.transactions if isinstance(t, Expense))
        print("\n===== All-Time Summary =====")
        print(f"Total Income : {income:.2f}")
        print(f"Total Expense: {expense:.2f}")
        print(f"Net Savings  : {income - expense:.2f}")
        print("============================")


# ------------------ CLI ------------------

def show_menu(balance: float) -> str:
    print("\n" + "=" * 34)
    print("     Personal Finance Tracker     ")
    print("=" * 34)
    print(f"Current Balance: Rs.{balance:.2f}")
    print("-" * 34)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Monthly Report")
    print("4. View All-time Summary")
    print("5. Exit")
    return input_prompt("Choose an option: ")


def read_amount() -> float:
    """Safely read a positive float amount from user."""
    while True:
        try:
            amt = float(input_prompt("Amount: "))
            if amt > 0:
                return amt
            print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid number.")


# ------------------ Main ------------------

def main() -> None:
    """Main program loop."""
    account = Account()
    rg = ReportGenerator()
    user_name = "Ayush"  #you can Write your name

    print("Welcome to Personal Finance Tracker!")

    while True:
        choice = show_menu(account.balance)

        if choice == "1":
            print("Adding Income...")
            amount = read_amount()
            category = input_prompt("Category: ")
            date_str = input_prompt("Date (DD-MM-YYYY): ")
            desc = input_prompt("Description (optional): ")
            try:
                date = parse_date(date_str)
                tx = Income(amount, category, date, desc)
                account.add(tx)
                print("Transaction added successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            print("Adding Expense...")
            amount = read_amount()
            category = input_prompt("Category: ")
            date_str = input_prompt("Date (DD-MM-YYYY): ")
            desc = input_prompt("Description (optional): ")
            try:
                date = parse_date(date_str)
                tx = Expense(amount, category, date, desc)
                account.add(tx)
                print("Transaction added successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            my = input_prompt("Enter month and year (MM-YYYY): ")
            if len(my) != 7 or my[2] != '-' or not my.replace('-', '').isdigit():
                print("Invalid format. Use MM-YYYY.")
                continue
            rg.print_monthly(account, my)

        elif choice == "4":
            rg.print_all_time(account)

        elif choice == "5":
            print(f"Have a Great Month, {user_name}!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
 
