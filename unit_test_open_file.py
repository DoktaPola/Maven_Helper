import os
import unittest
from unittest.mock import patch

from maven_helper import open_each_file

class TestMaven_Helper(unittest.TestCase):
    """Unit test for Maven helper"""

    @patch('os.walk')
    def test_open_each_file(self, walk):
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