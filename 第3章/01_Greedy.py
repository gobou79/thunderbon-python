import random
import copy

W = 4
H = 3
end_turn = 4

class Coord:
    def __init(self, y=0, x=0):
        self.y = y
        self.x = x

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
    

# ランダムに行動を決定する
def random_action(state):
    legal_actions = state.legal_actions()
    return random.choice(legal_actions)

# 貪欲法で行動を決定する
def greedy_action(state):
    legal_actions = state.legal_actions()
    best_score = -float('inf')
    best_action = -1
    for action in legal_actions:
        now_state = copy.deepcopy(state)
        now_state.advance(action)
        now_state.cal_evaluated_score()
        if now_state.evaluated_score > best_score:
            best_score = now_state.evaluated_score
            best_action = action
    return best_action

def play_game(seed):
    state = MazeState(seed)
    print(state.to_string())
    while not state.is_done():
        state.advance(greedy_action(state))
        print(state.to_string())

if __name__ == "__main__":
    play_game(seed = 121321)