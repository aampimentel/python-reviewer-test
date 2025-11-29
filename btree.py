class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t  # Minimum degree

    def traverse(self):
        """Traverses the tree and prints keys."""
        if self.root is not None:
            self._traverse(self.root)
        print()

    def _traverse(self, x):
        for i in range(len(x.keys)):
            if not x.leaf:
                self._traverse(x.children[i])
            print(x.keys[i], end=" ")
        if not x.leaf:
            self._traverse(x.children[len(x.keys)])

    def search(self, k):
        """Searches for a key in the tree."""
        return self._search(self.root, k)

    def _search(self, x, k):
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        if x.leaf:
            return None
        return self._search(x.children[i], k)

    def insert(self, k):
        """Inserts a new key into the B-Tree."""
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]

    def delete(self, k):
        """Deletes a key from the B-Tree."""
        self._delete(self.root, k)
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = BTreeNode(True)

    def _delete(self, x, k):
        t = self.t
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        
        if i < len(x.keys) and k == x.keys[i]:
            if x.leaf:
                x.keys.pop(i)
            else:
                y = x.children[i]
                z = x.children[i + 1]
                if len(y.keys) >= t:
                    pred = self._get_predecessor(y)
                    x.keys[i] = pred
                    self._delete(y, pred)
                elif len(z.keys) >= t:
                    succ = self._get_successor(z)
                    x.keys[i] = succ
                    self._delete(z, succ)
                else:
                    self._merge(x, i)
                    self._delete(y, k)
        elif not x.leaf:
            if len(x.children[i].keys) < t:
                self._fill(x, i)
            if i > len(x.keys): # Correct index if last child was merged
                self._delete(x.children[i-1], k)
            else:
                self._delete(x.children[i], k)

    def _get_predecessor(self, x):
        while not x.leaf:
            x = x.children[-1]
        return x.keys[-1]

    def _get_successor(self, x):
        while not x.leaf:
            x = x.children[0]
        return x.keys[0]

    def _fill(self, x, i):
        t = self.t
        if i != 0 and len(x.children[i - 1].keys) >= t:
            self._borrow_from_prev(x, i)
        elif i != len(x.keys) and len(x.children[i + 1].keys) >= t:
            self._borrow_from_next(x, i)
        else:
            if i != len(x.keys):
                self._merge(x, i)
            else:
                self._merge(x, i - 1)

    def _borrow_from_prev(self, x, i):
        child = x.children[i]
        sibling = x.children[i - 1]
        child.keys.insert(0, x.keys[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        x.keys[i - 1] = sibling.keys.pop()

    def _borrow_from_next(self, x, i):
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        x.keys[i] = sibling.keys.pop(0)

    def _merge(self, x, i):
        t = self.t
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys.pop(i))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        x.children.pop(i + 1)
