import unittest
import run

class test_run_py(unittest.TestCase):
    """Unit tests"""
    def test_calc_card_value(self):
        """Tests if the card value calculation is correct"""
        result = run.game.calc_value(["A♣", "10♣"], run.card_value)
        self.assertEqual(result, 21)

    def test_generate_deck(self):
        """
        Tests the generate deck function to make sure it 
        doesn't return none
        """
        result = run.game.generate_deck(1)
        self.assertIsNotNone(result)

    def test_hash_password(self):
        """Tests that password hashing doesn't return none"""
        result = run.account.hash_password("test")
        self.assertIsNotNone(result)
