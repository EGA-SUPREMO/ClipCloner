import unittest

from clip_generator.editter.compare_sound_by_images.offset import relation_percentage

class TestRelationPercentage(unittest.TestCase):
    def test_value1_greater_than_value2(self):
        value1 = 10
        value2 = 5
        expected_result = 66.66666666666666
        self.assertAlmostEqual(relation_percentage(value1, value2), expected_result)

    def test_value2_greater_than_value1(self):
        value1 = 5
        value2 = 10
        expected_result = 33.333333333333336
        self.assertAlmostEqual(relation_percentage(value1, value2), expected_result)

    def test_value1_equal_to_0(self):
        value1 = 0
        value2 = 5
        expected_result = 0.0
        self.assertAlmostEqual(relation_percentage(value1, value2), expected_result)

    def test_value2_equal_to_0(self):
        value1 = 5
        value2 = 0
        expected_result = 100.0
        self.assertAlmostEqual(relation_percentage(value1, value2), expected_result)

if __name__ == '__main__':
    unittest.main