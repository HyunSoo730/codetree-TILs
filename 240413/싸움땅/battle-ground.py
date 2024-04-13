import sys
from collections import defaultdict

# nxn 보드, 각 칸 무기 존재 or 빈칸,
# 초기 세팅 : 무기 없는 빈격자에 플레이어들이 위치, 초기 능력치 가짐(모두 다름) -> 따로 기록
# 각 칸은 총 공격력 나타내는 보드 -> 여러 개의 총이 존재 가능

# 라운드 진행
# 1-1. 1번부터 순차적으로 진행, 본인 방향으로 한칸 이동. 좌표 외부인 경우 반대방향으로 변경 후 1칸 이동
# 2-1. 이동한 방향에 플레이어 유무 확인
# 2-1-1. 플레이어 없음 -> 해당 칸 총 확인 -> 총 있는 경우 생각
# 총 있는 경우 -> 해당 플레이어 총 획득. 이미 총이 있으면 더 공격력이 센 총 획득, 나머지 해당 격자에 둠(교환)
# 2-1-2. 이동한 칸에 플레이어 존재 -> 싸움
# 현재 칸의 플레이어의 초기 능력치 + 가지고 있는 총의 공격력 합 비교, 더 큰 플레이어 승리
# 2-1-3. 해당 차이 같은 경우 -> 초기 능력치 높은 플레이어 승리
# 2-1-4. 이긴 플레이어는 초기 능력치와 가지고 있는 총의 공격력 합의 차이만큼 포인트 획득 (초기 능력치 - 총 공격력 합 차이)

# 2-1-5. 진 플레이어 본인 총 해당 격자에 내려놓기, 해당 플레이어가 원래 가지고 있던 방향대로 한 칸 이동
# 이동하려는 칸 플레이어 존재 or 외부 좌표 -> 시계 90도 지속 회전 빈칸 존재하면 이동.
# 해당 칸에 총 존재 -> 진 플레이어 가장 공격력이 높은 총 획득, 나머지 총 해당 격자에 내려 놓기(가장 공격력이 큰 총만 획득)

# 이 과정은 1~n번 플레이어 순차적으로 진행하면 1라운드 끝
# nxn, m명 플레이어, k라운드

n,m,k = map(int, input().split())
players = defaultdict(list) # 플레이어 정보 저장
player_score = [0] * (m+1) # 플레이어가 획득한 스코어 기록
g = [list(map(int, input().split())) for _ in range(n)] # 총 정보 기록
guns = defaultdict(list) # 좌표별 총을 기록
for x in range(n):
    for y in range(n):
        if g[x][y] > 0:
            guns[(x,y)].append(g[x][y]) # (x,y) 위치에 총 정보 기록

p = [[0] * n for _ in range(n)] # 플에이어 위치 정보 기록 보드
# g[x][y]에는 총의 공격력 기룍

for i in range(1,m+1): # 플레이어 정보, 초기 정보에는 총 X
    x,y,d,s = map(int, input().split()) # 플레이어 초기 위치, 초기 방향, 초기 능력치
    players[i] = [x-1,y-1,d,s,0] # 순서대로 기록, 4번 인덱스는 현재 플레이어의 총의 총격력
    p[x-1][y-1] = i # 해당 위치에 i번째 플레이어 존재

dx = [-1,0,1,0]
dy = [0,1,0,-1]
def isInner(x,y):
    if 0<=x<n and 0<=y<n:
        return True
    return False
def player_move(): # p 보드 갱신 추가
    global players
    for i in range(1,m+1):
        player = players[i] # 현재 이동할 플레이어 꺼낸 후
        x,y,dir,s,gun = player # 현재 플레이어 정보
        #  플레이어 이동
        nx,ny = x + dx[dir], y + dy[dir] # 이동 위치
        if not isInner(nx,ny): # 외부
            dir = (dir+2) % 4 # 방향 반대
            nx,ny = x + dx[dir], y + dy[dir] # 방향 바꿔서 이동
        #  이동한 위치 플레이어 유무 판단
        if p[nx][ny] == 0: # 플레이어 X
            if len(guns[(nx,ny)]) > 0: # 총 존재
                max_power = gun # 현재 총의 능력치
                flag = False # 갱신 하는지 체크
                for gun_power in guns[(nx,ny)]:  # 해당 위치에 존재하는 모든 총 확인
                    if gun_power > max_power:
                        max_power = gun_power
                        flag = True
                if flag: # 갱신 가능 하면
                    guns[(nx,ny)].remove(max_power)
                if flag and gun > 0: #  갱신 가능 하면서 이미 총 가지고 있는 경우
                    guns[(nx,ny)].append(gun)
                gun = max_power
            player = [nx,ny,dir,s,gun] # 정보 갱신
            players[i] = player
            p[x][y] = 0 # 기존 위치 플레이어 위치 없애고
            p[nx][ny] = i # 해당 플레이어 위치시키기
        else: # 플레이어 존재 -> 싸움
            target_idx = p[nx][ny] # 해당 위치에 존재하는 플레이어 번호
            target_player = players[target_idx]
            player_power = 능력치계산(s,gun)
            target_power = 능력치계산(target_player[3], target_player[4])
            win_idx = -1 # 이긴 사람의 인덱스 저장
            lose_idx = -1 # 진 사람 인덱스 저장
            if player_power > target_power:
                win_idx = i
                lose_idx = target_idx
            elif target_power > player_power:
                win_idx = target_idx
                lose_idx = i
            elif target_power == player_power:
                if s > target_player[3]:
                    win_idx = i
                    lose_idx = target_idx
                else:
                    win_idx = target_idx
                    lose_idx = i
            player_score[win_idx] += abs(player_power - target_power)  # 이긴 플레이어 행동 : 스코어 획득
            win_player = players[win_idx]
            lose_player = players[lose_idx]
            # 이긴 플레이어 총 정보 갱신
            max_power = win_player[4] # 기존정보를 맥스
            flag = False
            guns[(nx,ny)].append(lose_player[4]) # 일단 진 사람의 총도 추가
            guns[(nx,ny)].append(win_player[4]) # 이긴 사람 총도 추가.
            for gun_power in guns[(nx,ny)]: # 하나씩 꺼내서
                if gun_power > max_power:
                    max_power = gun_power
                    flag = True # 갱신 됨
            # 플레이어 위치 갱신
            p[win_player[0]][win_player[1]] = 0
            p[lose_player[0]][lose_player[1]] = 0

            players[win_idx] = [nx,ny,win_player[2],win_player[3],max_power] # 이긴 플레이어 갱신 -> 총 더 강한 거 주움
            p[nx][ny] = win_idx # 이긴 플레이어는 위치
            players[lose_idx] = [nx,ny,lose_player[2], lose_player[3], 0] # 일단 충돌 위치로 옮겨놓고
            진플레이어행동(lose_idx) # 진 플레이어의 기존 위치, 충돌날 위치 함께

            # 이긴 사람의 총 갱신 됐다면 삭제 후 내려놓기 진행
            if flag:
                guns[(nx,ny)].remove(max_power)

        # 본인 턴 종료 후 좌표, 방향, 능력치 등등 갱신해야함
        # print(f"현재 {i}번째 플레이어 끝나고 플레이어 위치 확인")
        # 플레이어위치확인()
        # print(f"현재 {i}번째 플레이어 끝나고 총 위치 확인")
        # 총위치확인(guns)

def 총위치확인(guns):
    for (x,y) , gun_list in guns.items():
        print(f"{x,y} 위치의 총 넘버 : {gun_list}")


def 플레이어위치확인():
    for player_num, val in players.items():
        print(f"{player_num}의 위치 : {val[0],val[1]} 방향 : {val[2]}, 기존능력치 :{val[3]}, 총 공격력 : {val[4]}")

def 진플레이어행동(lose_idx): # 본인 , 충돌난 위치
    # 본인 총 해당 격자에 내려놓기
    target = players[lose_idx]
    x,y,dir,s,gun = target
    if gun > 0: # 총 존재하면
        guns[(x,y)].append(gun) # 본인 총 해당 격자에 내려놓기
    gun = 0 # 본인 총 능력치 0으로 만들기
    # 방향 이동
    nx,ny = x,y
    direction = dir
    for i in range(4):
        direction = (dir + i) % 4
        nx = x + dx[direction]
        ny = y + dy[direction]
        if not isInner(nx,ny): continue
        if p[nx][ny] > 0: continue # 다른 플레이어 존재
        if p[nx][ny] == 0: # 해당 좌표 이동 가능 -> 빈칸 or 총 존재
            max_power = 0
            for gun_power in guns[(nx,ny)]: # 이동하려는 좌표의 총 정보 확인
                max_power = gun_power
            if max_power > 0: # 해당 격자에 총 존재
                guns[(nx,ny)].remove(max_power) # 지우고
                gun = max_power # 갱신
            p[nx][ny] = lose_idx # 이동 표시
            break # 이동하면 끝

    target = [nx,ny,direction,s,gun] # 마지막에 정보 갱신
    players[lose_idx] = target # 갱신




def 능력치계산(s,gun): # 초기 능력치,현재 가진 총의 능력치
    return s + gun

time = 0
while True:
    time += 1
    # print(f"{time} 라운드")

    player_move()

    if time == k:  # k라운드 진행. 종료조건
        break

print(*player_score[1:])