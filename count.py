import functools

print(functools.reduce(lambda s,n: s+int(n) if int(n)%2==0 else s, input().split(','), 0))