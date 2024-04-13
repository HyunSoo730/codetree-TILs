import sys
from collections import defaultdict


# 1~p명의 산타. 루돌프 1마리

# nxn 보드 (1,1) ~ (n,n), 게임은 총 M개의 턴.
# 루돌프 먼저 이동, 그 후 산타 1~P번 순서대로 이동 (기절하거나 탈락한 산타 제외)
#  두 칸 사이 거리 : (r1-r2)**2 + (c1-c2)**2

# 루돌프 움직임
# 1.루돌프는 게임에서 탈락하지 않은 산타 중 가장 가까운 산타에게 1칸 돌진
# 1-1.만약 가장 가까운 산타가 2명 이상
# 1-1-1. 행 좌표가 큰 산타에게 돌진, 행 좌표 동일 -> c좌표가 큰 산타에게 돌진 -> 튜플로 깔끔하게 비교 가능
# 1-1-2. 루돌프는 상하좌우,대각선 8방향 돌진, 가장 우선순위 높은 산타에게 가장 가까워지는 방향으로 한칸 돌진

# 산타 움직임
# 2. 산타는 1~P번 순서대로 움직임, 기절했거나 이미 탈락한 산타는 움직이지 않음
# 2-1. 산타는 루돌프에게 가까워지는 방향으로 1칸 이동.
# 2-2. 다른 산타가 있는 칸이나, 외부로 이동X
# 2-3. 가까워져야만 움직일 수 있음. 가까워지지 않으면 움직이지 않음 -> 거리 계산을 통해 판별
# 2-4. 산타는 상하좌우 중 한 곳 이동. 가장 가까워질 수 있는 방향이 여러개 -> 상 우 하 좌 우선순위에 맞게

# 충돌
# 3. 산타와 루돌프가 같은 칸 -> 충돌
# 3-1. 루돌프가 움직여 충돌 : 해당 산타 C만큼 점수 획득, 산타는 루돌프가 이동해온 방향(루돌프 방향)으로 C칸 밀려남
# 3-2. 산타가 움직여 충돌 : 해당 산타 D만큼 점수 획득, 산타는 본인 반대방향으로 D만큼 밀려남
# 3-3. 밀려난 위치 외부 : 게임 탈락
# 3-4. 밀려난 위치 다른 산타 : 상호작용

# 상호작용
# 4. 충돌 후 밀려난 위치에 다른 산타 -> 해당 산타는 이동해온 산타 방향으로 1칸 밀려남
# 4-1. 그 옆에서 계속 산타가 있다면 연쇄적으로 밀려남
# 4-2. 외부로 밀려나면 산타 탈락

# 기절
# 5. 산타는 충돌 후 기절. 다음 턴까지 기절. 그 다음 턴부터 정상
# 5-1. 기절하더라도 본인 스스로 못움직이지, 상호작용, 충돌 가능

# M번 턴 후 게임 끝
# *** P명 모두 탈락 시 게임 종료!!!
# 매 턴 이후 아직 탈락하지 않은 산타 1점씩 추가 점수
# 구하고자 : 게임이 끝났을 때 산타가 얻은 최종점수

# 위치 (0,0)부터 사용
n, m, p, C, D = map(int, input().split())  # nxn 보드, m번의 턴, p명의 산타, 스코어 C,D
a, b = map(int, input().split())  # 루돌프 초기 위치
dog = [a - 1, b - 1, 0]  # 루돌프 위치, 방향
santas = defaultdict(list)
santa_board = [[0] * n for _ in range(n)]  # 몇번 산타가 존재하는지 위치를 기록한 보드
for _ in range(p):
    num, x, y = map(int, input().split())
    santa_board[x - 1][y - 1] = num  # 산타 정보와 함께 싱크 잘 맞춰야함.
    santas[num] = [x - 1, y - 1, 0, 0, False]  # 산타의 위치, 방향, 기절 턴, 죽음 나타냄
santa_score = [0] * (p + 1)

def 거리계산(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

def isInner(x, y):
    if 0 <= x < n and 0 <= y < n:
        return True
    return False

def 가장가까운산타찾기():
    min_dis = int(1e9)
    santa_idx = -1
    for i in range(1, p + 1):
        santa = santas[i]
        if santa[4]: continue  # 죽은 경우 안돼
        dis = 거리계산(dog[0], dog[1], santa[0], santa[1])
        if dis < min_dis:
            santa_idx = i
            min_dis = dis
        elif dis == min_dis:
            target = santas[santa_idx]
            if (santa[0], santa[1]) > (target[0], target[1]):  # 행좌표우선, 열좌표우선
                santa_idx = i
    return santa_idx

루돌프이동x = [-1, -1, 0, 1, 1, 1, 0, -1]
루돌프이동y = [0, -1, -1, -1, 0, 1, 1, 1]

def isInner(x,y):
    if 0<=x<n and 0<=y<n:
        return True
    return False

def 루돌프이동():
    santa_idx = 가장가까운산타찾기()
    min_dis = int(1e9)
    target = santas[santa_idx]
    direction = 0
    for d in range(8):
        nx = dog[0] + 루돌프이동x[d]
        ny = dog[1] + 루돌프이동y[d]
        if not isInner(nx,ny):
            continue
        dis = 거리계산(nx,ny,target[0],target[1])
        if dis < min_dis:
            min_dis = dis
            direction = d
    # 루돌프 이동
    nx = dog[0] + 루돌프이동x[direction]
    ny = dog[1] + 루돌프이동y[direction]
    # 이동 후 싱크 맞춤 -> 루돌프 위치 갱신
    dog[0],dog[1] = nx,ny
    # 이동 후 충돌인지 확인
    if (dog[0], dog[1]) == (target[0],target[1]): # 충돌
        루돌프에의한충돌(santa_idx, direction)

def 루돌프에의한충돌(santa_idx, direction):
    santa = santas[santa_idx] # 충돌 산타
    santa_score[santa_idx] += C
    santas[santa_idx][3] = turn + 1
    산타밀려남(santa_idx, direction, C, 루돌프이동x[direction], 루돌프이동y[direction])

산타이동x = [-1,0,1,0]
산타이동y = [0,1,0,-1]
def 산타밀려남(santa_idx, direction, distance,dx,dy): # 해당 산타, direction 방향으로 distance 만큼 밀려남
    santa = santas[santa_idx]
    x,y = santa[0],santa[1] # 산타의 현재 위치
    santa_board[x][y] = 0 # 위치 갱신 진행

    nx = x + dx * distance
    ny = y + dy * distance # 산타가 밀려날 위치

    if not isInner(nx,ny): #  착지 위치가 외부 -> 다이
        santas[santa_idx][4] = True
        return
    while santa_board[nx][ny] > 0: # 밀려난 위치에 다른 산타가 있는 경우 -> 연쇄작용
        next_santa_idx = santa_board[nx][ny] # 다음 산타의 인덱스 저장
        santa_board[nx][ny] = santa_idx # 밀려난 위치에 다른 산타가 있을 때 해당 위치의 값을 현재 산타의 인덱스로 갱신
        santas[santa_idx][0],santas[santa_idx][1] = nx,ny # 산타정보 같이 갱신
        santa_idx = next_santa_idx # 산타를 다음 산타의 인덱스로 업데이트
        # 이렇게 하면 현재 산타가 밀려난 위치에 정보가 싱크되고 다음 산타의 인덱스를 따라가면서 연쇄적으로 밀려나는 과정을 처리

        nx += dx
        ny += dy
        if not isInner(nx,ny):
            santas[next_santa_idx][4] = True
            break # 이동한 위치 격자 밖이면 해당 산타 탈락, 종료

    # while 문 종료되면 최종 위치에 대해서도 산타 위치정보, 산타 정보 갱신
    santa_board[nx][ny] = santa_idx # 즉, 산타 위치 보드에 산타 인덱스 넣는 순간, 산타 정보에 해당 산타 인덱스 정보를 같이 갱신한다고 생각하자.
    santas[santa_idx][0],santas[santa_idx][1] = nx,ny

def 산타이동():
    for i in range(1,p+1):
        santa = santas[i]
        if santa[4]: continue
        if santa[3] >= turn: # 기절
            continue
        min_dis = 거리계산(dog[0],dog[1],santa[0],santa[1])
        direction = -1
        for k in range(4):
            nx = santa[0] + 산타이동x[k]
            ny = santa[1] + 산타이동y[k]
            if not isInner(nx,ny): continue
            if santa_board[nx][ny] > 0: continue # 다른 산타 위치
            dis = 거리계산(dog[0],dog[1], nx,ny)
            if dis < min_dis:
                min_dis = dis
                direction = k
        if direction != -1:
            nx = santa[0] + 산타이동x[direction]
            ny = santa[1] + 산타이동y[direction]
            santa_board[santa[0]][santa[1]] = 0 #
            santa_board[nx][ny] = i # 산타 위치 갱신
            santa[0],santa[1],santa[2] = nx,ny,direction # 산타 정보 갱신
            santas[i] = santa
            if (dog[0],dog[1]) == (nx,ny): # 산타에 의한 충돌
                산타에의한충돌(i)


def 산타에의한충돌(santa_idx):
    santa = santas[santa_idx]
    santa_score[santa_idx] += D
    direction = (santa[2] + 2) % 4 # 반대 방향
    santas[santa_idx][3] = turn + 1 # 기절 상태 업데이트 turn + 1까지는 기절
    산타밀려남(santa_idx, direction, D,산타이동x[direction], 산타이동y[direction])


def 루돌프이동후위치확인():
    print(f"현재 루돌프위치 : {dog[0],dog[1]}")

def 산타이동후위치확인():
    for i in range(n):
        for j in range(n):
            print(santa_board[i][j], end = " ")
        print()


for turn in range(1,m+1):
    # print(f"========={turn}라운드 진행=================")
    루돌프이동()
    # 루돌프이동후위치확인()
    산타이동()
    # print(f"산타 이동 후 위치")
    # 산타이동후위치확인()
    for i in range(1, p + 1):
        if santas[i][4]: continue
        santa_score[i] += 1

print(*santa_score[1:])