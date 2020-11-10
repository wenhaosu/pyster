# Sample Python program including two simple classes

from objin import Foo
from runtime.test import magic

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

    print("My new {} account has ${}.".format(savings.kind, savings.balance))
    print("My new {} account has ${}.".format(checking.kind, checking.balance))
    print(savings.status())

    wages = 800
    savings.deposit(wages)

    cash = savings.withdraw(150)
    checking.deposit(cash)
    test = savings.test(["test_string", "anothor_one"])
    print(test)
    test = savings.test_obj(Foo("name"))
    print(test)

    print("I deposited ${} into my {} account.".format(wages, savings.kind))
    print("I transferred ${} from {} to {}.".format(cash, savings.kind,
                                                checking.kind))
    print()

    print("My {} account now has ${}.".format(savings.kind, savings.balance))
    print("My {} account now has ${}.".format(checking.kind, checking.balance))


if __name__ == "__main__":
    with magic([BankAccount]):
        main()
