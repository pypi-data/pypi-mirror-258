import unittest
from Spannotation.main_module import calculate_drivable_area

class TestMainModule(unittest.TestCase):

    def test_calculate_drivable_area(self):
     
        points = [(0, 0), (10, 0), (5, 5)]

        # Call the function you're testing
        result = calculate_drivable_area(points)

        # Assert expected outcome
        expected_area = 25  
        self.assertEqual(result, expected_area)

# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()



