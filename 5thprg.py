import functools
string1='1729'
print(functools.reduce(lambda s,n:int(n)+s, string1, 0))