import random

H = 3   #迷路の高さ
W = 4   #迷路の幅
end_turn = 4    #ゲームの終了ターン

class Coord:
    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x

class MazeState:
    dx = [1, -1, 0, 0]  #右、左、下、上への移動方向のx成分
    dy = [0, 0, 1, -1]  #右、左、下、上への移動方向のx成分

    def __init__(self, seed):
        random.seed(seed)
        self.points = [[0 for _ in range(W)] for __ in range(H)]
        self.turn = 0   #現在のターン
        self.character = Coord()
        self.game_score = 0 #ゲーム上で実際に得たスコア

        self.character.y = random.randint(0, H-1)
        self.character.x = random.randint(0, W-1)

        for y in range(H):
            for x in range(W):
                if y == self.character.y and x == self.character.x:
                    continue
                self.points[y][x] = random.randint(0, 9)
    
    def is_done(self):
        return self.turn == end_turn
    
    def advance(self, action):
        self.character.x += self.dx[action]
        self.character.y += self.dy[action]
        point = self.points[self.character.y][self.character.x]
        if point > 0:
            self.game_score += point
            self.points[self.character.y][self.character.x] = 0
        self.turn += 1
    
    def legal_actions(self):
        actions = [
            action for action in range(4) 
            if 0 <= self.character.y + self.dy[action] < H 
            and 0 <= self.character.x + self.dx[action] < W]
        return actions
    
    def to_string(self):
        result = []
        result.append(f"turn:\t{self.turn}")
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
    
# randomに行動を決定する
def random_action(state):
    legal_actions = state.legal_actions()
    return random.choice(legal_actions)

# シードを指定してゲーム状況を表示しながらAIにプレイさせる
def play_game(seed):
    state = MazeState(seed)
    print(state.to_string())
    while not state.is_done():
        state.advance(random_action(state))
        print(state.to_string())

if __name__ == "__main__":
    play_game(seed=121321)