import unittest

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from src.util.list_utils import ListUtils
from tests.util.test_utils import TestUtils


class ListUtilsTest(unittest.TestCase):
    def test_powerset(self):
        expected = [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
        result = ListUtils().powerset([1,2,3])
        self.assertEqual(expected, result)

    def test_combination(self):
        expected = [[1,1,3],[1,1,4],[1,2,3],[1,2,4],[2,1,3],[2,1,4],[2,2,3],[2,2,4]]
        result = ListUtils().combination([[1,2],[1,2],[3,4]])
        TestUtils(self).assertListContentEqualIgnoringOrder(expected, result)

    def test_combination_single_node(self):
        expected = [[1]]
        result = ListUtils().combination([[1]])
        TestUtils(self).assertListContentEqualIgnoringOrder(expected, result)

    def test_combination_similar_content(self):
        expected = [[1,1],[1,1],[1,1],[1,1]]
        result = ListUtils().combination([[1,1],[1,1]])
        TestUtils(self).assertListContentEqualIgnoringOrder(expected, result)