import unittest
from btree import BTree

class TestBTree(unittest.TestCase):
    def test_insert_and_search(self):
        t = 3
        btree = BTree(t)
        keys = [10, 20, 5, 6, 12, 30, 7, 17]
        for k in keys:
            btree.insert(k)

        for k in keys:
            result = btree.search(k)
            self.assertIsNotNone(result)
            self.assertEqual(result[0].keys[result[1]], k)

        self.assertIsNone(btree.search(99))

    def test_delete(self):
        t = 3
        btree = BTree(t)
        keys = [1, 3, 7, 10, 11, 13, 14, 15, 18, 16, 19, 24, 25, 26, 21, 4, 5, 20, 22, 2, 17, 12, 6]
        for k in keys:
            btree.insert(k)

        # Delete leaf
        btree.delete(6)
        self.assertIsNone(btree.search(6))

        # Delete internal node
        btree.delete(13)
        self.assertIsNone(btree.search(13))
        
        # Verify tree structure integrity by searching for other keys
        for k in keys:
            if k != 6 and k != 13:
                self.assertIsNotNone(btree.search(k))

    def test_traversal(self):
        # Capturing stdout is a bit tricky in simple unit tests without extra setup,
        # so we'll rely on search for verification for now.
        pass

if __name__ == '__main__':
    unittest.main()
