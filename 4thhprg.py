lis=['orange','apple','banana','ManGo','appricot']
print(list(map(lambda x: x if x[0].lower()=='a' else '',lis)))
print(list(filter(lambda x: x[0].lower()=='a', lis)))