import unittest
import run

class test_run_py(unittest.TestCase):
    
    def test_calc_card_value(self):
        result = run.game.calc_value(["A♣", "10♣"], run.card_value)
        self.assertEqual(result, 21)