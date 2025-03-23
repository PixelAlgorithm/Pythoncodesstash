'''
given list of circleS area all in five decimal places,round each element in list up to tw

'''


def roundoff(lis,pos=[0]):
    pos.append(1)
    return [round(lis,len(pos))]

print([*map(roundoff,[3.14159, 2.71828, 1.41421])])