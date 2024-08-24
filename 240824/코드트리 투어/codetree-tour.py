import heapq
from collections import defaultdict


def 건설(n, m, arr):
    global g, N
    N = n  # 전역 변수 N을 업데이트합니다.
    g = [[INF] * N for _ in range(N)]
    for i in range(N):
        g[i][i] = 0
    for i in range(m):
        a, b, c = arr[i*3], arr[i*3+1], arr[i*3+2]
        g[a][b] = min(g[a][b], c)
        g[b][a] = min(g[b][a], c)

def 여행상품추가(id, revenue, dest):
    global isMade, 여행상품
    isMade[id] = True
    이익 = revenue - dis[dest]
    heapq.heappush(여행상품, (-이익, id))

def 상품취소(id):
    global isCancel
    if isMade[id]:
        isCancel[id] = True

def 상품판매():
    global 여행상품, isCancel
    while 여행상품:
        이익, id = -여행상품[0][0], 여행상품[0][1]
        if 이익 < 0:
            break
        heapq.heappop(여행상품)
        if not isCancel[id]:
            return id
    return -1

def 시작도시변경(now):
    global start
    start = now
    dijkstra()
    temp = []
    while 여행상품:
        _, id = heapq.heappop(여행상품)
        temp.append(id)
    for id in temp:
        revenue, dest = 상품정보[id]
        여행상품추가(id, revenue, dest)

def dijkstra():
    global dis
    dis = [INF] * N
    q = [(0, start)]
    dis[start] = 0

    while q:
        distance, now = heapq.heappop(q)
        if dis[now] < distance:
            continue
        for v in range(N):
            if g[now][v] == INF:
                continue
            cost = distance + g[now][v]
            if cost < dis[v]:
                dis[v] = cost
                heapq.heappush(q, (cost, v))

T = int(input())
INF = int(1e9)
start = 0
dis = []
g = []
N = 0  # 도시의 수를 저장할 전역 변수
isMade = [False] * 30001
isCancel = [False] * 30001
여행상품 = []
상품정보 = defaultdict(tuple)

for _ in range(T):
    commands = list(map(int, input().split()))
    command = commands[0]
    if command == 100:
        건설(commands[1], commands[2], commands[3:])
        dijkstra()
    elif command == 200:
        id, revenue, dest = commands[1], commands[2], commands[3]
        상품정보[id] = (revenue, dest)
        여행상품추가(id, revenue, dest)
    elif command == 300:
        id = commands[1]
        상품취소(id)
    elif command == 400:
        res = 상품판매()
        print(res)
    elif command == 500:
        시작도시변경(commands[1])