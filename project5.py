
c=open('Testing1.txt',mode='r+')
c.write('Hi testing')

d=c.read()
c.close()

print(d)