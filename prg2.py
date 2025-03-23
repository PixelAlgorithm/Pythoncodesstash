class bank():
    def __init__(self, name, accountno,balance):
        self.name = name
        self.balance = balance
        self.accountno = accountno
    def deposit(self,amount):
        self.balance += amount
    def withdraw(self,amount):
        if amount>self.balance:
            print('Insufficient balance')
        else:
            print('Withdrawal of',amount,'is successful')
            self.balance -= amount
    def display(self):
        print('Name:',self.name)
        print('Account number:',self.accountno)
        print('Balance:',self.balance)
    def balance(self):
        print(self.balance)



print('Enter the name, account number and balance of the account holder')
ob1=bank(input(),int(input()),int(input()))
while True:
    print('Enter choice 1.Deposit 2.Withdraw 3.Display 4.Balance')
    ch=int(input())
    if ch==1:
        ob1.deposit(int(input('Enter the amount to be deposited')))
    elif ch==2:
        ob1.withdraw(int(input('Enter the amount to be withdrawn')))
    elif ch==3:
        ob1.display()
    elif ch==4:
        print(ob1.balance)
    elif ch==5:
        break