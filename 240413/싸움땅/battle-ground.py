import sys
from collections import defaultdict

# nxn 보드
# 초기 세팅 : 무기 없는 빈격자에 플레이어들이 위치, 초기 능력치 가짐(모두 다름) -> 따로 기록
# 각 칸은 총 공격력 나타내는 보드 -> 여러 개의 총이 존재 가능

# 라운드 진행
# 1-1. 1번 플레이어부터 순차적으로 진행, 본인 방향으로 한칸 이동. 좌표 외부인 경우 반대방향으로 변경 후 1칸 이동
# 2-1. 이동한 방향에 플레이어 유무 확인
# 2-1-1. 플레이어 없음 -> 해당 칸 총 확인 -> 총 있는 경우 생각
# 총 있는 경우 -> 해당 플레이어 총 획득. 이미 총이 있으면 더 공격력이 센 총 획득, 나머지 해당 격자에 둠(교환)
# 2-1-2. 이동한 칸에 플레이어 존재 -> 싸움
# 현재 칸의 플레이어의 초기 능력치 + 가지고 있는 총의 공격력 합 비교, 더 큰 플레이어 승리
# 2-1-3. 해당 차이 같은 경우 -> 초기 능력치 높은 플레이어 승리
# 2-1-4. 이긴 플레이어는 초기 능력치와 가지고 있는 총의 공격력 합의 차이만큼 포인트 획득 (초기 능력치 - 총 공격력 합 차이)
# 2-1-5. 진 플레이어 본인 총 해당 격자에 내려놓기, 해당 플레이어가 원래 가지고 있던 방향대로 한 칸 이동
# 2-1-6. 이긴 플레이어는 총 능력치 최신화
# 2-1-7. 진 플레이어가 이동하려는 칸 플레이어 존재 or 외부 좌표 -> 시계 90도 지속 회전 빈칸 존재하면 이동.
# 해당 칸에 총 존재 -> 가장 능력치 높은 총 획득, 나머지 총 해당 격자에 내려 놓기(가장 공격력이 큰 총만 획득)

# 이 과정을 1~n번 플레이어 순차적으로 진행하면 1라운드 끝
# nxn, m명 플레이어, k라운드


n,m,k = map(int, input().split())
players = defaultdict(list) # 플레이어 정보 딕셔너리로 저장
player_score = [0] * (m+1) # 플레이어가 획득한 스코어 기록
g = [list(map(int, input().split())) for _ in range(n)] # 총 정보
guns = defaultdict(list) # 좌표별 총을 기록
for x in range(n):
    for y in range(n):
        if g[x][y] > 0:
            guns[(x,y)].append(g[x][y]) # (x,y) 위치에 총 정보 기록
p = [[0] * n for _ in range(n)] # 플에이어 위치 정보 기록 보드

# 이동이 일어날 때마다 플레이어 위치 정보를 기록하는 p 보드, 플레이어 정보 players 싱크 맞추면서 진행
for i in range(1,m+1): # 플레이어 정보, 초기 정보에는 총 X
    x,y,d,s = map(int, input().split()) # 플레이어 초기 위치, 초기 방향, 초기 능력치
    players[i] = [x-1,y-1,d,s,0] # 순서대로 기록, 4번 인덱스는 현재 플레이어의 총의 총격력
    p[x-1][y-1] = i # 해당 위치에 i번째 플레이어 존재한다는 뜻

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
        #  step1. 플레이어 이동
        nx,ny = x + dx[dir], y + dy[dir] # 이동 위치
        if not isInner(nx,ny): # 외부
            dir = (dir+2) % 4 # 방향 반대
            nx,ny = x + dx[dir], y + dy[dir] # 방향 바꿔서 이동

        # 현재 플레이어 위치 방향 수정
        p[x][y] = 0 # 이동 전 위치 미리 삭제
        players[i] = [nx,ny,dir,s,gun]
        player = players[i]

        #  step2. 이동한 위치 플레이어 유무 판단
        if p[nx][ny] == 0: # 플레이어 X
            if len(guns[(nx,ny)]) > 0: # 총 존재
                gun_list = guns[(nx,ny)]
                gun_list.sort() # 공격력 오름차순 정렬
                if gun_list[-1] > gun: # 기존 총보다 크면 갱신
                    players[i][4] = gun_list[-1] # 최대값으로 갱신
                    gun_list.pop() # 마지막 제거 후
                    gun_list.append(gun) # 기존 값 추가
                    guns[(nx,ny)] = gun_list # 갱신
            p[nx][ny] = i # 위치 갱신
        else: # 플레이어 존재
            target_idx = p[nx][ny] # 해당 위치에 존재하는 플레이어 번호
            target_player = players[target_idx]
            player_power = 능력치계산(player[3], player[4])
            target_power = 능력치계산(target_player[3], target_player[4])
            win_idx = -1 # 이긴 사람의 인덱스 저장
            lose_idx = -1 # 진 사람 인덱스 저장

            # 이긴사람, 진 사람 인덱스 확인
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
            # 이긴사람 점수 추가
            player_score[win_idx] += abs(player_power - target_power)  # 이긴 플레이어 행동 : 스코어 획득
            win_player = players[win_idx]
            lose_player = players[lose_idx]

            # 이긴 플레이어 총 능력치 갱신, 진 사람 총 내려둠
            max_power = win_player[4] # 기존정보를 맥스
            if lose_player[4] > 0:
                guns[(nx,ny)].append(lose_player[4])
            if guns[(nx,ny)]:
                guns[(nx,ny)].sort()
                if guns[(nx,ny)][-1] > max_power: # 갱신
                    max_power = guns[(nx,ny)][-1]
                    guns[(nx,ny)].pop()
                    guns[(nx,ny)].append(win_player[4]) # 기존값 추가

            # 플레이어 위치 갱신 (이동 전 위치는 미리 없앰)
            players[win_idx][4] = max_power # 갱신
            p[nx][ny] = win_idx # 이긴 플레이어 위치 갱신
            players[lose_idx][4] = 0 # 진 사람 총 초기화
            진플레이어행동(lose_idx) # 진 플레이어의 기존 위치, 충돌날 위치 함께


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
    target = players[lose_idx]
    x,y,dir,s,gun = target
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
            if guns[(nx,ny)]: # 존재하면
                guns[(nx,ny)].sort()
                max_power = guns[(nx,ny)][-1]
                gun = max_power
                guns[(nx,ny)].pop() # 제거
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