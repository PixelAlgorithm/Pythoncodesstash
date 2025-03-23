matrix=[[]]
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

mat_trans = [[0 for i in range(len(matrix))] for j in range(len(matrix[0]))]
print(mat_trans)
print()
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        mat_trans[j][i] = matrix[i][j]

print(mat_trans)