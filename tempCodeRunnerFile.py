t=7
summ=0
l=[2,3,6,7]
s=[[] for _ in range(len(l))]
for i in range(0,len(l)):
    print(i)
    for j in l[i+1::]:
        if (summ<t and summ+j<=t):
            summ=sum(s[i])+j
            s[i].append(j)
        else:
            continue

print(s)