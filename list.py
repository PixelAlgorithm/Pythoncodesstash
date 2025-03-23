import functools


print(functools.reduce(lambda x,y:x+y, ['hello','world','python','java']))

'''
def gcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

'''

def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)
print(functools.reduce(gcd, [36,60,48,96]))