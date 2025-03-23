'''ing: Item name (string), Price (float) and 
Quantity (integer) separated by spaces'''


import functools

n = int(input())
items = [input().split() for _ in range(n)]

num_items = len(list(filter(lambda x: int(x[2]) > 0, items)))
total_cost = functools.reduce(lambda acc, x: acc + float(x[1]) * int(x[2]), items, 0)
most_expensive = max(items, key=lambda x: float(x[1]))

print(f"Number of available items: {num_items}")
print(f"Total cart value: ${total_cost:.2f}")
print(f"Most expensive item: {most_expensive[0]} (${most_expensive[1]})")
 