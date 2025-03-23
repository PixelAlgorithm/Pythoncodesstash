scores=[60,70,80,90,100]
print([i for i in scores if i>=75])

#using filter

print(list(filter(lambda x: x>=75, scores)))


