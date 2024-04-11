def bfs_chat(c, child, auth, alam):
    q = []
    q.insert(0, (c, 0))
    cnt=0
    while len(q)>0:
        now = q.pop()
        for ch in child[now[0]]:
            # print("ch", ch, "alam", alam[ch-1]!=0, "auth : ", now[1] <= auth[ch-1]-1)
            if alam[ch-1]==0 : # 알람이 꺼져있으면 세지 않는다.
                continue
            if now[1] <= auth[ch-1]-1 : # depth차이 > 권한 power 이면 닿지 않는다.
                cnt+=1
            q.insert(0, (ch, now[1]+1))
    return cnt
def power(auth, c, to):
    auth[c-1] = to
def onoff(alam, c):
    alam[c-1] ^=1 
def swap(c1, c2, origin_p, origin_c):
    global n
    c1 -=1 ;   c2 -=1
    p = origin_p.copy()
    c = origin_c.copy()
    # 부모 변경
    p[c1] = origin_p[c2]
    p[c2] = origin_p[c1]
    # c1,c2부모의 자식 교환
    c[origin_p[c1]].remove(c1+1)
    c[origin_p[c1]].append(c2+1)
    c[origin_p[c2]].remove(c2+1)
    c[origin_p[c2]].append(c1+1)
    return p, c


n, q = map(int, input().split())
auth = []
parent = []
child = [[] for _ in range(0, n+1)]
alam = [1 for _ in range(n)]    
#100 명령은 항상 첫 번째 명령으로만 주어지며, 항상 주어집니다. 0번 채팅방의 p값과 a값은 주어지지 않음에 유의합니다.
command = list(map(int, input().split()))
parent = command[1:n+1]
auth = command[n+1:]
for i in range(n) : 
    p = parent[i]
    child[p].append(i+1)
for _ in range(q-1):
    command = list(map(int, input().split()))
    if command[0] == 200:
        onoff(alam, command[1])
    elif command[0] == 300 : 
        power(auth, command[1], int(command[2]))
    elif command[0] == 400 :
        parent, child = swap(command[1], command[2], parent, child)
    elif command[0] == 500 : 
        print(command, alam)
        print(bfs_chat(command[1], child, auth, alam))