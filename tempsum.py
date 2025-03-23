import functools
l=input('Enter the list of numbers: ').split(',')
s=functools.reduce(lambda x,y:int(x)+int(y),l)
avg=int(s)/len(l)
print('Sum : ' ,s)
print('The average of the list of numbers is:',avg)
print(f'Maximum {functools.reduce(lambda x,y:x if x>y else y,l)}')


