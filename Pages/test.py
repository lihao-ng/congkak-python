import copy

test = [1, 2, 3, 4, 5, 6]
x = 0
tcp = copy.deepcopy(test)
z = 0

def addition(u):
    u += u
    return u

def delEle(array, index):
    array.pop(index)
    ntcp = copy.deepcopy(array)
    print("array at delEle is now "+str(ntcp))

for i in tcp:
    x = 6
    if i == 1:
        x = addition(x)
    print(x)
    #print(tcp)
    #delEle(tcp, i)






    # z += 1
    # if i == z:
    #     ntcp = copy.deepcopy(test)
    #     for i in ntcp:
    #         if i == z:
    #             print("element at index "+str(i)+" is "+str(ntcp[i]))
    #             ntcp.pop(i)
    #             print("the array is now this after removing i"+str(ntcp))
        #x = 6
    #print(x)