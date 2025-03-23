l = list(map(int,input('Enter Numbers ').split(',')))
print(f'Even no : {list(filter(lambda x: x%2==0,l))} \n Odd no : {list(filter(lambda x: x%2!=0,l))}')
