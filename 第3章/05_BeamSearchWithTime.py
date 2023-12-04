import random
import heapq
import copy
import time

W = 30
H = 30
end_turn = 100

class Coord:
    def __init(self, y=0, x=0):
        self.y = y
        self.x = x

class TimeKeeper:
    def __init__(self, time_threshold):
        self.start_time = time.time()
        self.time_threshold = time_threshold
    
    def is_time_over(self):
        current_time = time.time()
        return (current_time - self.start_time) * 1000 >= self.time_threshold

class MazeState:
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    def __init__(self, seed):
        random.seed(seed)
        self.points = [[0 for _ in range(W)] for _ in range(H)]
        self.turn = 0
        self.character = Coord()
        self.game_score = 0
        self.evaluated_score = 0
        self.first_action = -1  # 探索木のルートノードで最初に選択した行動

        self.character.y = random.randint(0, H-1)
        self.character.x = random.randint(0, W-1)

        for y in range(H):
            for x in range(W):
                if y == self.character.y and x == self.character.x:
                    continue
                self.points[y][x] = random.randint(0, 9)
    
    def is_done(self):
        return self.turn == end_turn

    def cal_evaluated_score(self):
        self.evaluated_score = self.game_score

    def advance(self, action):
        self.character.x += self.dx[action]
        self.character.y += self.dy[action]
        point = self.points[self.character.y][self.character.x]
        if point > 0:
            self.game_score += point
            self.points[self.character.y][self.character.x] = 0
        self.turn += 1

    def legal_actions(self):
        actions = [action for action in range(4) if 0 <= self.character.y + self.dy[action] < H and 0 <= self.character.x + self.dx[action] < W]
        return actions
    
    def to_string(self):
        result = []
        result.append(f"turn: \t{self.turn}")
        result.append(f"score:\t{self.game_score}")
        for h in range(H):
            row = ''
            for w in range(W):
                if self.character.y == h and self.character.x == w:
                    row += '@'
                elif self.points[h][w] > 0:
                    row += str(self.points[h][w])
                else:
                    row += '.'
            result.append(row)
        return '\n'.join(result)
    
    # 探索時のソート用に評価を比較する
    def __lt__(self, other):
        return other.evaluated_score < self.evaluated_score

# ビーム幅と制限時間(ms)を指定してビームサーチで行動を決定する
def beam_search_action_with_time_threshold(
        state, 
        beam_width, 
        time_threshold
    ):
    time_keeper = TimeKeeper(time_threshold)
    now_beam = [state]
    best_state = state

    for t in range(end_turn):
        next_beam = []
        for i in range(beam_width):
            if time_keeper.is_time_over():
                return best_state.first_action
            if not now_beam:
                break
            now_state = heapq.heappop(now_beam)
            legal_actions = now_state.legal_actions()
            for action in legal_actions:
                next_state = copy.deepcopy(now_state)
                next_state.advance(action)
                next_state.cal_evaluated_score()
                if t == 0:
                    next_state.first_action = action
                heapq.heappush(next_beam, next_state)
        
        now_beam = copy.copy(next_beam)
        best_state = now_beam[0]

        if best_state.is_done():
            break
    return best_state.first_action

# ゲームをgame_number回プレイして平均スコアを表示する
def test_ai_score(game_number):
    score_mean = 0
    for i in range(game_number):
        state = MazeState(random.randint(0, 10000))
        while not state.is_done():
            state.advance(beam_search_action_with_time_threshold(state, 5, 2))
        score_mean += state.game_score
    score_mean /= game_number
    print(f"Score:\t{score_mean}")

if __name__ == "__main__":
    test_ai_score(100)