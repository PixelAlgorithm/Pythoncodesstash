import functools

def mul(a,b):
    print(f'a {a} b {b}')
    print(a*b)
    return(a*b)



print(functools.reduce(mul, [1,2,3,4,5],100)) 
print('add:')
print(functools.reduce(lambda x,y:max(x,y), [1,2,3,4]))
print(functools.reduce(lambda x,y:x if x>y else y, [1,2,3,22,4]))