matrix=[[1,2],[3,4],[5,6],[7,8]]


transpose=list(zip(*matrix))

print([[i[j] for i in matrix] for j in range(2)])

print(transpose)


mattrans=[]