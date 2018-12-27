import os
import unittest
from unittest.mock import patch

from maven_helper import zipdir


class TestMaven_Helper(unittest.TestCase):
    """Unit test for Maven helper"""

    @patch('zipfile.ZipFile')
    def test_zipdir(self, ZipFile):
        """unit test when archive from folders with files can be created"""
        ar_name = r'new_zip_file.zip'
        pom_file = 'my_pom.pom'


        walk.return_value = [
            (path, (), ('test.txt', pom_file, 'abc.doc')),
        ]
        actual_res = find_pom(path)
        expected_res = os.path.join(path, pom_file)
        self.assertEqual(actual_res, expected_res)

