import os
import unittest
from unittest.mock import patch

from new import find_pom
from new import open_each_file
# from new import get_version
from new import make_rec
from new import find_difference


class TestMaven_Helper(unittest.TestCase):
    """Unit test for Maven helper"""

    @patch('os.walk')
    def test_find_pom(self, walk):
        """unit test when .pom is in path"""
        path = 'path'
        pom_file = 'my_pom.pom'
        walk.return_value = [
            (path, (), ('test.txt', pom_file, 'abc.doc')),
        ]
        actual_res = find_pom(path)
        expected_res = os.path.join(path, pom_file)
        self.assertEqual(actual_res, expected_res)

    @patch('os.walk')
    def test_find_pom_several(self, walk):
        """unit test when several .pom are in path"""
        path = 'path'
        pom_files = ('my_pom.pom', 'second_pom.pom')
        walk.return_value = [
            (path, (), pom_files)
        ]
        self.assertRaises(ValueError, find_pom, path)

    @patch('os.walk')
    def test_no_pom(self, walk):
        """unit test when .pom is not in the path"""
        path = 'path'
        pom_file = ()
        walk.return_value = [
            (path, (), pom_file)
        ]
        self.assertRaises(ValueError, find_pom, path)
# @patch('new.my_func')
# def test_my_func(self, fun):
#     """unit test when several .pom are in path"""
#     fun.return_value = 'bbb'
#     another_func()

# def test_open_each_file(self):
#     self.assertEqual(result[i], expected_res[i])
#
# def test_make_rec(self):
#     self.assertEqual(result[i], expected_res[i])
#
# def test_find_difference(self):
#     self.assertEqual(result[i], expected_res[i])

# def test_empty_array(self):
#     self.assertEqual(selection_sort([]), 'array is empty')

#
# if __name__ == '__main__':
#     unittest.main()
