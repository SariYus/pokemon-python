import unittest
import pytest
from client import update_type, get_pokemon_by_type


class MyTestCase(unittest.TestCase):
    def test_update_type(self):
        print("a:", get_pokemon_by_type("normal"))
        self.assertTrue("eevee" in get_pokemon_by_type("normal"))


if __name__ == '__main__':
    unittest.main()
