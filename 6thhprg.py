import functools
l=[1,2,3,4,5]
print(min(l))
print(functools.reduce(lambda x,y:x if x<y else y,l))
