def changedItem(col):
    array = []
    for i in range(len(col.index)):
        if col.loc[i] == False:
            array.append(i)
    return array

def printItems(refarray, index):
    pass    