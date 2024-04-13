'''
기사 이동
- 상하좌우 한칸 이동
- 기사의 연쇄이동(방향대로 한칸씩)

대결 
- (밀친기사x) 밀려나게된 기사가 방패범위내 함정 수만큼 피해
- 체력이 동나면 사라짐

총 받은 데미지의 합 더하기
단, 처음 주어지는 기사들의 위치는 기사들끼리 서로 겹쳐져 있지 않습니다. 
또한 기사와 벽은 겹쳐서 주어지지 않습니다.

'''
l, n, q = map(int, input().split())
array = []
dx = [-1,0,1,0]
dy = [0,1,0,-1]
array.append([2,])
knights = [[],]
health = [0,]
origin = [0,]
knmap= []

def move(num, d):
    stack = [num,]
    visit = [num,]
    while len(stack)>0:
        now = stack.pop()
        block=False
        temp = []
        for body in knights[now]:
            nx = body[0]+dx[d]
            ny = body[1]+dy[d]
            if nx < 1 or ny < 1 or nx > l or ny > l : continue
            if array[nx][ny] == 2 : 
                block = True
                continue # 벽이라 더이상 이동x
            if knmap[nx][ny] > 0 : # 기사와 마주치는 경우
                if knmap[nx][ny] in visit : continue
                temp.append(knmap[nx][ny])
        if not block  :
            stack.extend(temp)
            visit.extend(temp)     
    # print("q : ", num, visit)
    # 마지막 밀려나는 기사부터 이동
    block = False
    temp = []
    for i in range(len(visit)-1, -1, -1):
        if block : break
        for body in knights[visit[i]]:
            nx = body[0]+dx[d]
            ny = body[1]+dy[d]
            if nx < 1 or ny < 1 or nx > l or ny > l : 
                block = True
                continue
            if array[nx][ny] == 2 : 
                block = True
                continue # 벽이라 더이상 이동x
        if not block : 
            test = []
            temp.append(visit[i])
            for body in knights[visit[i]]:
                nx = body[0]+dx[d]
                ny = body[1]+dy[d]
                knmap[nx][ny] = visit[i]
                knmap[body[0]][body[1]] = 0 #이동
                test.append((nx, ny))
            knights[visit[i]] = test            
    # print("real move", temp)
    if num in temp : 
        temp.remove(num)
    return temp

def damege(realmoved):
    # 이동이 끝난 후 체력 검사, 0 이하이면 탈락시킴
    if len(realmoved)==0 : return
    for i in realmoved:
        for body in knights[i]:
            if array[body[0]][body[1]]==1:
                health[i]-=1
        if health[i]<= 0 : 
            for body in knights[i]:
                array[body[0]][body[1]] = 0
            knights[i] = []
    return
for i in range(l):
    array[0].append(2)
    array.append(list(map(int, input().split())))
    array[i+1].insert(0, 2)
knmap = [[0 for _ in range(l+1)] for _ in range(l+1)]
for i in range(n):
    r,c,h,w,k = map(int, input().split())
    temp = []
    health.append(k)
    origin.append(k)
    for j in range(h) :
        for x in range(w) :
            temp.append((r+j, c+x))
            knmap[r+j][c+x] = i+1
    knights.append(temp)

# print(array)
# print(knmap)

for i in range(q):
    num, d = map(int, input().split())
    realmoved = move(num, d)
    damege(realmoved)
    
# print(knmap)
# print(knights)

total = 0
for i in range(1, n+1):
    if health[i] <= 0 : continue
    else : 
        total += (origin[i]-health[i])

# print(origin)
# print(health)
print(total)