arr = [[0 for _ in range(10)] for _ in range(10)]
def Putable(row, col, dir, len):
    #Out of bound
    if dir=="竖":
        if row+len>10:
            #print("out of bound"+str(col)+str(row))
            return False
        i=row
        while i<len+row:
            if arr[i][col]!=0:
                #print("repeat"+str(col)+str(row))
                return False
            i += 1
        return True


    if dir=="横":
        if col+len>10:
            #print("out of bound"+str(col)+str(row))
            return False
        i=col
        while i<len+col:
            if arr[row][i]!=0:
                #print("Repeat"+str(col)+str(row))
                return False
            i += 1
    return True
def put_Miss(row, col, dir, len):
    if Putable(row, col, dir, len):
        if dir=="竖":
            i = row
            while i < len + row:
                arr[i][col]="M"
                i+=1
        if dir=="横":
            i=col
            while i<len+col:
                arr[row][i]="M"
                i+=1
def put(row, col, dir, len):
    if Putable(row, col, dir, len):
        if dir=="竖":
            i = row
            while i < len + row:
                arr[i][col]="H"
                i+=1
        if dir=="横":
            i=col
            while i<len+col:
                arr[row][i]="H"
                i+=1
def put1(row, col, dir, len, map):
    if Putable(row, col, dir, len):
        if dir=="竖":
            i=row
            while i < len + row:
                map[i][col]+=1
                i+=1
        if dir=="横":
            i=col
            while i<len+col:
                map[row][i]+=1
                i+=1



def prob_map(length):
    map1=[[0 for _ in range(10)] for _ in range(10)]
    for i in range(0,10):
        for j in range(0,10):
            if Putable(i,j,"横",length):
                put1(i,j,"横",length,map1)
            if Putable(i,j,"竖",length):
                put1(i,j,"竖",length,map1)
    for i in range(10):
        print(map1[i])
    return map1

def maxnum(map):
    max_num=0
    x=0
    y=0
    for i in range(10):
        for j in range(10):
            if map[i][j]>max_num:
                max_num=map[i][j]
                x=j+1
                y=i+1
    print("x:"+str(x))
    print("y:"+str(y))
userx=0
while userx!=99:
    userx=int(input("your first shot, x-axis, press 99 if you want to quit, press 999 if you need help"))
    if userx==999:
        length_of=int(input("The length of your target ship?"))
        maxnum(prob_map(length_of))
        continue
    usery=int(input("your first shot, y-axis"))
    put(usery-1,userx-1, "竖", 1)
    for i in range(10):
        print(arr[i])