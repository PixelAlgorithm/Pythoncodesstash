import functools
print(len([i for i in 'hello one space ' if i==' ']))

#remove all vowels in a string


print(''.join([i for i in 'hello one space ' if i not in 'aeiou']))


print(functools.reduce(lambda c,s: c+s if s not in 'aeiou' else c, 'hello one space ', ''))


z


