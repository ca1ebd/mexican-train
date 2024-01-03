import unittest

from Game import Game
from Player import Player
from Domino import Domino, OldLady
from Train import Train, CommonTrain

class TestGameClass(unittest.TestCase):
    def setUp(self):
        player1 = Player("player1")
        player2 = Player("player2")
        # Create an instance of the Person class for testing
        self.game = Game(num_rounds=9, players=[player1, player2])
        self.original_pool = self.game._generate_dominoes(9)
        self.shuffled_pool = self.game._shuffle_pool(self.original_pool.copy())

    def tearDown(self):
        # Clean up any resources used for testing
        pass

    def test_pool_generator(self):
        # Test the getter for name attribute

        # test correct number of dominoes
        self.assertEqual(len(self.original_pool), 55)

        counts = {x: 0 for x in range(0, 10)}
        # test there are 11 appearances of each number
        for domino in self.original_pool:
            counts[domino.left] += 1
            counts[domino.right] += 1

        for count_key in counts.keys():
            self.assertEqual(counts[count_key], 11, f"There are {counts[count_key]} {count_key}'s found on dominoes")

    def test_shuffle(self):
        pool = self.shuffled_pool

        # test correct number of dominoes
        self.assertEqual(len(pool), 55)

        counts = {x: 0 for x in range(0, 10)}
        # test there are 11 appearances of each number
        for domino in pool:
            counts[domino.left] += 1
            counts[domino.right] += 1

        for count_key in counts.keys():
            self.assertEqual(counts[count_key], 11, f"There are {counts[count_key]} {count_key}'s found on dominoes")

class TestDominoClass(unittest.TestCase):
    def setUp(self):
        self.dom1 = Domino(3, 4)
        self.dom1_copy = Domino(3, 4)
        self.dom1_swap = Domino(4, 3)

        self.dom2 = Domino(5, 6)
        self.dom3 = Domino(6, 7)

        self.old_lady = OldLady()

    def tearDown(self):
        # Clean up any resources used for testing
        pass

    def test_domino_equality(self):
        # test __eq__ override
        self.assertEqual(self.dom1, self.dom1_copy)
        self.assertEqual(self.dom1, self.dom1_swap)

    def test_score(self):
        self.assertEqual(self.dom1.score(), 7)
        self.assertEqual(self.dom2.score(), 11)
        self.assertEqual(self.dom3.score(), 13)

        self.assertEqual(self.dom1.score(), self.dom1_copy.score())
        self.assertEqual(self.dom1.score(), self.dom1_swap.score())

        self.assertLess(self.dom1.score(), self.dom2.score())
        self.assertLess(self.dom2.score(), self.dom3.score())
        self.assertLess(self.dom3.score(), self.old_lady.score())

    def test_old_lady(self):
        self.assertEqual(self.old_lady.left, 0)
        self.assertEqual(self.old_lady.right, 0)

        self.assertEqual(self.old_lady.score(), 50)

class TestTrainClass(unittest.TestCase):
    def setUp(self):
        self.t1 = Train("TestTrain1", tip=9)
        self.t1_copy = Train("TestTrain1", tip=7)

        self.t2 = CommonTrain(tip=6)

    def tearDown(self):
        # Clean up any resources used for testing
        pass

    def test_train_equality(self):
        # test __eq__ override
        self.assertEqual(self.t1, self.t1_copy)
        self.assertNotEqual(self.t1, self.t2)

    def test_public(self):
        self.assertFalse(self.t1.is_public())
        self.assertTrue(self.t2.is_public())

        self.t1.set_public(True)
        self.assertTrue(self.t1.is_public())

    def test_add_domino(self):
        d_9_2 = Domino(9, 2)
        d_3_2 = Domino(3, 2)

        self.t1.add_domino(d_9_2)
        self.assertEqual(self.t1.tip, 2)

        self.t1.add_domino(d_3_2)
        self.assertEqual(self.t1.tip, 3)

        self.assertIn(d_9_2, self.t1.dominoes)
        self.assertIn(d_3_2, self.t1.dominoes)

    def test_reset(self):
        self.t1.reset(8)
        self.assertEqual(self.t1.dominoes, [])
        self.assertEqual(self.t1.tip, 8)

        self.t1.add_domino(Domino(7, 8))
        self.assertEqual(self.t1.tip, 7)

        self.t1.add_domino(Domino(3, 7))
        self.assertEqual(self.t1.tip, 3)
        self.assertEqual(len(self.t1.dominoes), 2)


if __name__ == "__main__":
    unittest.main()