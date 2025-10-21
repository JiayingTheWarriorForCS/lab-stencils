import unittest
from marginal_value import calculate_marginal_value

class TestMarginalValue(unittest.TestCase):

    def test_example_case(self):
        goods = {"A", "B"}
        bids = {"A": 95, "B": 90}
        prices = {"A": 80, "B": 80}

        def valuation(bundle):
            if "A" in bundle and "B" in bundle:
                return 100
            elif "A" in bundle:
                return 90
            elif "B" in bundle:
                return 70
            return 0

        mv_a = calculate_marginal_value(goods, "A", valuation, bids, prices)

        expected_mv_a = 30

        self.assertAlmostEqual(mv_a, expected_mv_a, places=3, msg=f"Incorrect marginal value for A: expected {expected_mv_a}, got {mv_a}")


    def test_no_goods_won(self):
        goods = {"A", "B"}
        bids = {"A": 50, "B": 50}
        prices = {"A": 100, "B": 100}

        def valuation(bundle): 
            return len(bundle) * 10 

        mv_a = calculate_marginal_value(goods, "A", valuation, bids, prices)
        mv_b = calculate_marginal_value(goods, "B", valuation, bids, prices)

        self.assertEqual(mv_a, 10, "Incorrect marginal value for A")
        self.assertEqual(mv_b, 10, "Incorrect marginal value for B")

    #TODO: Fill in test cases
    def test_student_case_1(self):
        """Student test case 1: Test when bidder wins all goods with additive valuation"""
        
        goods = {"A", "B", "C"}
        bids = {"A": 100, "B": 80, "C": 60}
        prices = {"A": 50, "B": 70, "C": 55}

        def student_valuation(bundle):
            # Simple additive valuation: A=50, B=40, C=30
            values = {"A": 50, "B": 40, "C": 30}
            return sum(values.get(item, 0) for item in bundle)

        mv_a = calculate_marginal_value(goods, "A", student_valuation, bids, prices)

        self.assertEqual(mv_a, 50, "Marginal value of A should be 50 in additive valuation")

    def test_student_case_2(self):
        """Student test case 2: Test complement valuation where goods work better together"""
        
        goods = {"X", "Y", "Z"}
        bids = {"X": 60, "Y": 40, "Z": 20}
        prices = {"X": 50, "Y": 35, "Z": 25}

        def student_valuation(bundle):
            # Complement valuation: X and Y together are worth more than sum of parts
            if "X" in bundle and "Y" in bundle and "Z" in bundle:
                return 120  # Strong complement effect
            elif "X" in bundle and "Y" in bundle:
                return 90   # Complement effect for X+Y
            elif "X" in bundle:
                return 40
            elif "Y" in bundle:
                return 30
            elif "Z" in bundle:
                return 15
            return 0

        mv_x = calculate_marginal_value(goods, "X", student_valuation, bids, prices)

        # When bidder wins X and Y (but not Z since bid < price), 
        # marginal value of X = valuation({X,Y}) - valuation({Y}) = 90 - 30 = 60
        self.assertEqual(mv_x, 60, "Marginal value of X with complement effect should be 60")
    
    def test_student_case_3(self):
        """Student test case 3: Test substitute valuation with diminishing returns"""
        
        goods = {"P", "Q", "R"}
        bids = {"P": 70, "Q": 50, "R": 30}
        prices = {"P": 60, "Q": 45, "R": 35}

        def student_valuation(bundle):
            # Substitute valuation: goods are substitutes with diminishing returns
            # Having multiple similar goods reduces their individual value
            base_values = {"P": 50, "Q": 40, "R": 25}
            if not bundle:
                return 0
            
            total_value = 0
            for item in bundle:
                total_value += base_values.get(item, 0)
            
            # Apply diminishing returns: each additional item is worth less
            discount_factor = 0.8 ** (len(bundle) - 1)
            return total_value * discount_factor

        mv_q = calculate_marginal_value(goods, "Q", student_valuation, bids, prices)

        # Bidder wins P and Q (but not R since bid < price)
        # Marginal value of Q = valuation({P,Q}) - valuation({P})
        # valuation({P,Q}) = (50+40) * 0.8 = 72
        # valuation({P}) = 50 * 1.0 = 50
        # So mv_q = 72 - 50 = 22
        self.assertEqual(mv_q, 22, "Marginal value of Q with substitute effect should be 22")


if __name__ == "__main__":
    unittest.main()
