import os
def cl():
    os.system('cls')
cl()
class password():
    def __init__(self,name,age,hobby) :
        self.name=name
        self.age=age
        self.hobby=hobby
    def add(self):
        self.sum=self.age+2
        print(self.sum)

a=password(input('Enter Name :\t'),int(input('Enter Age :\t')),hobby=input('Enter hobby :\t'))
cl()
print(f'Printing Your Information:\nName :\t{a.name}\nAge:\t{a.age}\nHobby:\t{a.hobby}')
a.add()
