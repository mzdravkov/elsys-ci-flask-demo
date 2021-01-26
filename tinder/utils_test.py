import unittest
from . import utils

class UtilsTest(unittest.TestCase):
    def test_hash_password(self):
        assert 'fc5a1047f5919892fcdf8aa79ea5d6bb6531b5c176939ef0110906cb225941c1' == utils.hash_password('llama')

if __name__ == '__main__':
    unittest.main()
