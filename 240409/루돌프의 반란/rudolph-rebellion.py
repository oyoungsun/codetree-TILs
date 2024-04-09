import sys, math
#루 -> 산(살아있는것만)
# 거리 (x)^2+y^2
def roo(santa, rx, ry):
    global p, lastDir
    minD = sys.maxsize
    minx, miny, num = 0,0,0
    for i in range(1, p+1): # 가장 가까운 산타를 구한다.
        if i not in santa : continue
        dist = distance(santa[i][0], santa[i][1], rx, ry)
        if(minD >= dist):
            if(minD==dist):
                if minx < santa[i][0]: # r 우선 비교
                    num=i
                    minx, miny = santa[i][0:2]
                    continue
                elif minx==santa[i][0] and miny < santa[i][1]: # r같은 경우, c 비교
                    num=i
                    minx, miny = santa[i][0:2]
                    continue
                else : 
                    continue # r이 minx가 더 큼 -> 변경x
            else : 
                minD=dist
                num=i
                minx, miny = santa[i][0:2]
    #산타를 향해 1칸 이동한다. (2*2*2)
    ox,oy = rx,ry
    if minx > rx: 
        rx += 1
    elif minx < rx : 
        rx -= 1
    if miny > ry :
        ry += 1
    elif miny < ry : 
        ry -= 1
    lastDir[0] = [rx-ox, ry-oy] # 루돌프와 부딪히면 산타는 루돌프 방향으로 밀려난다.
    # print("roo ", rx, ry, num, lastDir[0])
    return rx, ry

def distance(x,y,r,w):
    return  math.pow(r-x,2)+ math.pow(w-y, 2) 

def san(santa, score, rx, ry, sanmap):
    global n, lastDir, p
    # direction = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    direction = [[0,-1], [1, 0], [0, 1], [-1, 0]]
    #루돌프에게 가까워지는 방향으로 이동
    #조건에 해당하지 않으면 가만히
    #상>우>하>좌
    for i in range(1, p+1):
        if i not in santa : continue
        if santa[i][2]==1 : 
            santa[i][2]+=1
            continue
        if santa[i][2]==2 : 
            santa[i][2]=0 # 기절 끝
        nx, ny = santa[i][0:2]
        # 상하좌우로 이동한 거리랑 루돌프랑 거리 최소
        dist= sys.maxsize
        nextx, nexty = nx,ny
        for d in direction:
            nextx = nx+d[0]
            nexty = ny+d[1]
            if nextx < 1 or nexty < 1 or nextx > n or nexty > n : 
                continue # 이동할 수 없다
            if sanmap[nextx][nexty] > 0 : 
                continue # 다른 산타 있음
            if dist >= distance(nextx, nexty, rx, ry): # 상
                dist = distance(nextx, nexty, rx, ry)
                lastDir[i] = [d[0]*-1, d[1]*-1] # 방향 반대로 저장 
                santa[i][0:2] = nextx, nexty 
        if nextx == santa[i][0] and nexty==santa[i][1] : 
            continue # 이동할 수 없다
        sanmap[santa[i][0]][santa[i][1]] = i #next
        sanmap[nx][ny] = 0 # origin
        # if(i==2):
        #     print(sanmap[3], sanmap[4], "sanma")
    # print("next : ", santa)
    # print("lastDir", lastDir)

def collaps(santa, rx, ry, isSanta): # 산타와 루돌프의 충돌을 검사
    global c,d, p
    for i in range(1, p+1):
        if i not in santa : continue
        if(santa[i][0]!=rx or santa[i][1]!=ry) : continue
        santa[i][2] = 1 # 기절 1회차
        move = d if isSanta else c
        score[i] += move
        #santa 밀기
        x, y = santa[i][0:2]
        sanmap[x][y]=0
        t = i if isSanta else 0 # 움직일 방향(산타 반대 or 루돌프 이동방향)
        santa[i][0:2] = [x + move * lastDir[t][0], y + move * lastDir[t][1]] # lastDir[t] 방향으로 이동
        nx, ny = santa[i][0:2]
        # print("score + ", "d" if isSanta else "c", i,":",nx,ny)
        if nx < 1 or ny < 1 or nx > n or ny > n : 
            v = santa.pop(i) # 산타 제거
            sanmap[x][y]=0
            # print("deleted by roo", i, v)
            continue
        # print("score + ", "d" if isSanta else "c", i,":",nx,ny, sanmap[nx][ny])
        if(sanmap[nx][ny] > 0) : 
            meet(sanmap[nx][ny], nx, ny, lastDir[i])
        sanmap[nx][ny]=i # 산타 이동 완료
        # print("pushed 완", santa[2], sanmap[santa[2][0]])
    return
def meet(wasStay, x, y, dirs):
    global santa, sanmap
    #밀려나서 산타가 두명이 만난다면
    #가만히 있던 산타가 한칸 밀림
    #재귀로 구현 santa[wasStay][0:1]
    if wasStay not in santa : return
    nx, ny = [x + dirs[0], y + dirs[1]]
    if nx < 1 or ny < 1 or nx > n or ny > n : 
        v = santa.pop(wasStay) # 산타 제거
        sanmap[x][y]=0
        # print("deleted by push", i, v)
        return
    if sanmap[nx][ny] > 0 : # 다른 산타 밀기
        meet(sanmap[nx][ny], nx,ny, dirs)
    sanmap[nx][ny] = wasStay  # 밀리기 완료
    santa[wasStay][0:2] = nx,ny
    # print("pushed ", wasStay, santa[2], sanmap[santa[2][0]])
    return

def isDone(turn, m, santa):
    if turn == m : 
        return True
    if len(santa)==0 :
         return True
    #산타가 모두 탈락
    #또는 m턴 모두 이동
    return False
def doneOfTurn(santa, score):
    for i in range(1, p+1):
        if i in santa:
            score[i]+=1
    return

n,m,p,c,d = map(int, input().split())

rx, ry = map(int, input().split())
arr = [[0 for _ in range(n+1)] for _ in range(n+1)]
santa = {}
score = [0 for _ in range(0, p+1)]
sanmap = [[0 for _ in range(n+1)] for _ in range(n+1)]
lastDir = [[] for _ in range(0, p+1)]
for i in range(p):
    num, sx, sy = map(int, input().split())
    santa[num] = [sx,sy, 0] # 위치, 기절 여부
    sanmap[sx][sy]=i

turn=0
# print("prev:", santa)
while(not isDone(turn, m, santa)):
    rx, ry = roo(santa, rx,ry) # 루돌프 이동
    collaps(santa, rx, ry, False) # 루돌프와 산타 충돌 판단
    san(santa, score, rx, ry, sanmap) # 산타 이동
    collaps(santa, rx, ry, True) # 루돌프와 산타 충돌 판단
    doneOfTurn(santa, score) # 한 턴 종료
    # break
    # print(" ".join(str(s) for s in score[1:]))
    turn+=1
print(" ".join(str(s) for s in score[1:]))