# This file is where game logic lives. No input
# or output happens here. The logic in this file
# should be unit-testable.

import random

class TicTacToeGame:
    def __init__(self, player1, player2):
        self.board = [[None, None, None] for _ in range(3)]
        self.current_player = player1
        self.other_player = player2

    def play_turn(self):
        x, y = self.current_player.make_move(self.board)

        if self.board[x][y] is not None:
            raise ValueError(f"The spot ({x}, {y}) is already taken.")

        self.board[x][y] = self.current_player.marker
        self.current_player, self.other_player = self.other_player, self.current_player

    def get_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        return None

    def is_draw(self):
        return all(all(cell is not None for cell in row) for row in self.board)

class Player:
    def __init__(self, marker):
        self.marker = marker

    def make_move(self, board):
        x, y = map(int, input(f"Enter the position of (x,y) for {self.marker}, split with comma: ").split(","))
        return x, y

class Bot(Player):
    def make_move(self, board):
        empty_spots = [(x, y) for x in range(3) for y in range(3) if board[x][y] is None]
        return random.choice(empty_spots) if empty_spots else (0, 0)

def print_board(board):
    print("  0 1 2")
    for i, row in enumerate(board):
        print_row = [cell if cell is not None else ' ' for cell in row]
        print(f"{i} {' '.join(print_row)}")

def main():
    player1 = Player('X')
    player2 = Bot('O')
    game = TicTacToeGame(player1, player2)

    while True:
        print_board(game.board)
        game.play_turn()
        winner = game.get_winner()
        if winner:
            print_board(game.board)
            print(f"Player {winner} wins!")
            break
        if game.is_draw():
            print_board(game.board)
            print("It's a draw!")
            break

if __name__ == '__main__':
    main()

import random
import csv
import os

class TicTacToeGame:
    def __init__(self, player1, player2, database_file):
        self.board = [[None, None, None] for _ in range(3)]
        self.current_player = player1
        self.other_player = player2
        self.database_file = database_file
        self.log_data = []  # Additional data to be logged

    def play_turn(self):
        x, y = self.current_player.make_move(self.board)

        if self.board[x][y] is not None:
            raise ValueError(f"The spot ({x}, {y}) is already taken.")

        self.board[x][y] = self.current_player.marker

        # Log the move
        self.log_data.append({
            'player': self.current_player.marker,
            'move': (x, y)
        })

        self.current_player, self.other_player = self.other_player, self.current_player

    def get_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        return None

    def is_draw(self):
        return all(all(cell is not None for cell in row) for row in self.board)

    def record_winner(self, winner):
        if winner:
            with open(self.database_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([winner])

            # Log additional data
            self.log_data[-1]['winner'] = winner

    def save_log(self, log_file):
        with open(log_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['player', 'move', 'winner'])
            writer.writeheader()
            writer.writerows(self.log_data)

class Player:
    def __init__(self, marker, name):
        self.marker = marker
        self.name = name

    def make_move(self, board):
        x, y = map(int, input(f"{self.name}, enter the position of (x,y) for {self.marker}, split with comma: ").split(","))
        return x, y

class Bot(Player):
    def make_move(self, board):
        empty_spots = [(x, y) for x in range(3) for y in range(3) if board[x][y] is None]
        return random.choice(empty_spots) if empty_spots else (0, 0)

class HumanPlayer(Player):
    def make_move(self, board):
        x, y = super().make_move(board)
        self.record_winner(board, self.marker)
        return x, y

    def record_winner(self, board, marker):
        winner = self.check_winner(board, marker)
        if winner:
            with open(self.log_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['winner', 'player1', 'player2'])
                writer.writerow({
                    'winner': winner,
                    'player1': self.name if self.marker == 'X' else self.other_player.name,
                    'player2': self.other_player.name if self.marker == 'X' else self.name,
                })

    def check_winner(self, board, marker):
        # Add logic to check for a winner in the current board state
        # (similar to the existing check_winner method in TicTacToeGame)
        # Return the winner marker if there is one, otherwise return None
        for row in board:
            if row[0] == row[1] == row[2] and row[0] == marker:
                return marker

        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] == marker:
                return marker

        if board[0][0] == board[1][1] == board[2][2] and board[0][0] == marker:
            return marker
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] == marker:
            return marker

        return None

def print_board_to_file(board, file):
    with open(file, 'a') as f:
        f.write("  0 1 2\n")
        for i, row in enumerate(board):
            print_row = [cell if cell is not None else ' ' for cell in row]
            f.write(f"{i} {' '.join(print_row)}\n")

def main():
    logs_directory = 'logs'
    os.makedirs(logs_directory, exist_ok=True)
    database_file = os.path.join(logs_directory, 'winners.csv')
    log_file = os.path.join(logs_directory, 'game_log.csv')
    board_file = os.path.join(logs_directory, 'game_board.txt')

    player1 = Player('X', 'Player 1')
    player2 = Bot('O', 'Bot 1')
    game = TicTacToeGame(player1, player2, database_file)

    while True:
        print_board_to_file(game.board, board_file)
        game.play_turn()
        winner = game.get_winner()
        if winner:
            game.record_winner(winner)
            game.save_log(log_file)
            print_board_to_file(game.board, board_file)
            with open(board_file, 'a') as f:
                f.write(f"{player1.name}: {len([data['winner'] for data in game.log_data if data['winner'] == player1.marker])} wins\n")
                f.write(f"{player2.name}: {len([data['winner'] for data in game.log_data if data['winner'] == player2.marker])} wins\n")
                f.write(f"Total Games: {len(game.log_data)}\n")
                f.write(f"Draws: {len([data['winner'] for data in game.log_data if data['winner'] is None])}\n")
            break
        if game.is_draw():
            game.save_log(log_file)
            print_board_to_file(game.board, board_file)
            with open(board_file, 'a') as f:
                f.write("It's a draw!\n")
            break

if __name__ == '__main__':
    main()