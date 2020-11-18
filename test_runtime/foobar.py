# Sample Python program including two simple classes

import objin
from runtime.test_runtime import pyster

class BankAccount:
    def __init__(self, kind: str):
        self.kind = kind
        self.balance = 0
        self.overdraft_fees = 0

    def deposit(self, amount: int):
        self.balance += amount

    def withdraw(self, amount: int):
        self.balance -= amount
        if self.balance < 0:
            self.overdraft_fees += 20
        return amount

    def status(self):
        return self.kind

    def test(self, input_list: list):
        return self.kind

    def test_obj(self, input_obj: any):
        return self.kind

def main():

    savings = BankAccount("savings")
    checking = BankAccount("checking")

    print(savings.status())

    wages = 800
    savings.deposit(wages)

    cash = savings.withdraw(150)
    checking.deposit(cash)
    test = savings.test(["test_string", "anothor_one"])
    test = savings.test_obj(objin.Foo("name"))


if __name__ == "__main__":
    with pyster([BankAccount]):
        main()
