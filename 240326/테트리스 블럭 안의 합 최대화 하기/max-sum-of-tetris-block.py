import sys


n, m = map(int, input().split())

g = [list(map(int, input().split())) for _ in range(n)]

# ! 3가지에 대해서 모든 경우 구하기
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
max_sum = 0


def isInner(x, y):
    if 0 <= x < n and 0 <= y < m:
        return True
    return False


def can_go(x, y):
    global visited
    if isInner(x, y) and (x, y) not in visited:
        return True
    return False


def DFS(L, now_sum):
    global max_sum
    if L == 4:  # ! 4칸 확인
        max_sum = max(max_sum, now_sum)
    else:
        for (x, y) in visited:  # ! 인접한 좌표들로부터 꺼내야지 -> 즉 주어진 좌표에 대해 가능한 모든 모양을 탐색
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if can_go(nx,ny): # ! 해당 좌표 내부에 있으면서 아직 방문 안했으면
                    visited.append((nx,ny))
                    DFS(L+1, now_sum + g[nx][ny])
                    visited.pop()

visited = []
for x in range(n):
    for y in range(m):
        visited.append((x, y))  # ! 현재 좌표
        DFS(1, g[x][y])
        visited.pop()

print(max_sum)