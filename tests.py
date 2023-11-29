import unittest
from logic import TicTacToeGame, HumanPlayer, BotPlayer

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        self.player1 = HumanPlayer("X")
        self.player2 = HumanPlayer("O")
        self.bot = BotPlayer("O")
        self.game = TicTacToeGame(self.player1, self.player2)

    def test_initial_board(self):
        expected_board = [[None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(self.game.get_board(), expected_board, "Initial board should be empty")

    def test_play_turn(self):
        # Mock player input to control the test
        self.player1.make_move = lambda board: (0, 0)
        self.game.play_turn()
        self.assertEqual(self.game.get_board()[0][0], "X", "First cell should be marked 'X'")

        # Change turn to player 2 and play
        self.player2.make_move = lambda board: (0, 1)
        self.game.play_turn()
        self.assertEqual(self.game.get_board()[0][1], "O", "Second cell should be marked 'O'")

    def test_get_winner(self):
        # Test for row, column, and diagonal wins
        winning_states = [
            ([["X", "X", "X"], [None, None, None], [None, None, None]], "X"),
            ([["O", None, None], ["O", None, None], ["O", None, None]], "O"),
            ([["X", None, None], [None, "X", None], [None, None, "X"]], "X")
        ]
        for board_state, winner in winning_states:
            self.game.set_board(board_state)
            self.assertEqual(self.game.get_winner(), winner)

    def test_is_draw(self):
        self.game.set_board([["X", "O", "X"], ["X", "X", "O"], ["O", "X", "O"]])
        self.assertTrue(self.game.is_draw(), "Game should be a draw")

    def test_bot_move(self):
        # Ensure bot chooses a valid empty spot
        self.game.set_board([["X", "O", "X"], ["X", "X", "O"], ["O", None, "O"]])
        x, y = self.bot.make_move(self.game.get_board())
        self.assertIsNone(self.game.get_board()[x][y], "Selected spot by bot should be empty")

        # Test bot's choice when only one spot is left
        self.game.set_board([["X", "O", "X"], ["X", "X", "O"], ["O", "X", None]])
        x, y = self.bot.make_move(self.game.get_board())
        self.assertEqual((x, y), (2, 2), "Bot should choose the last remaining spot")

    def test_no_winner(self):
        self.game.set_board([["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]])
        self.assertIsNone(self.game.get_winner(), "There should be no winner")

    def test_invalid_move(self):
        # Test for a scenario where a player tries to play on a non-empty spot
        self.game.set_board([["X", None, None], [None, None, None], [None, None, None]])
        self.player1.make_move = lambda board: (0, 0)  # Try to place on an already occupied spot
        with self.assertRaises(ValueError):  # You may need to modify your game logic to raise an exception in this case
            self.game.play_turn()

if __name__ == '__main__':
    unittest.main()