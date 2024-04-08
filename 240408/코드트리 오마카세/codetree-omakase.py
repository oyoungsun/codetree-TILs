def doEat(prev, now):
    global l, sushi, people, time
    for t in range(prev+1, now+1):
        if t in time : 
            for comman in time[t] : 
                name, x= comman[2], comman[1]
                if(comman[0]==1) : 
                        if(name not in sushi):
                            sushi[name] = dict()
                            sushi[name][(l+x-(t%5)) % 5] = 1
                        elif ((l+x-(t%5)) % 5) not in sushi[name].keys(): 
                            sushi[name][(l+x-(t%5)) % 5]= 1
                        else : 
                            sushi[name][(l+x-(t%5)) % 5]+= 1
                else : 
                    n = comman[3]
                    people[name] = [x, n]
        # 먹기
        for name, info in people.items() : 
            x = info[0]
            for sx in sushi[name].keys():
                if (sx+t)%l == x : 
                    # print("name peo1", people[name], sushi[name])
                    eat = min(info[1], sushi[name][sx]) #먹어야 하는 개수, 남은 개수 중 더 작은것으로 둘다 적용
                    people[name]=[x, info[1]-eat]
                    sushi[name][sx]-=eat
                    # print("name peo2", people[name], sushi[name])
            # sx = (l+info[0] - (t%l))%l
            # if sx in sushi[name].keys() : 
                

prev=0
l, q = map(int, input().split())
people = dict() # 사람당 위치, 먹어야하는 초밥 수
# 초밥(이름) 당 위치(t=0일때 위치): 개수
sushi = dict()
time = dict()
for comman in range(q):
    c = input().split()
    if(c[0]=="100"): #만들기
        t, x, name = int(c[1]), int(c[2]), c[3]
        if t not in time : 
            time[t] = []
        time[t].append((1, x, name))
    elif(c[0]=="200"): #입장
        t, x, name, n = int(c[1]), int(c[2]), c[3], int(c[4])
        if t not in time : 
            time[t] = []
        time[t].append((2, x, name, n))
    else : #사진
        t = int(c[1])
        doEat(prev, t)
        prev=t
        psum=0
        ssum=0
        for k,v in people.items():
            if(v[1] > 0 ):
                psum+=1
        for k, v in sushi.items():
            for key, value in v.items():
                if value<=0 : continue
                ssum+=value
        print(psum, ssum)