# Implementation of Segment Trees in Python
# No Lazy Propogation

def merge(left_node, right_node):
    """
    Returns the node obtained by merging
    left_node and right_node
    """
    merged_node = Node(0)
    if not left_node:
        left_node = Node(0)
    if not right_node:
        right_node = Node(0)
    merged_node.val = left_node.val + right_node.val
    return merged_node


class Node(object):
    """
    A segment tree node.
    """

    def __init__(self, val=0):
        self.val = val

class SegmentTree(object):
    """
    A segment tree
    """

    def __init__(self, arr):
        self.arr = arr
        self.start = 0
        self.end = len(arr)-1
        self.tree_size = 2 * len(arr) - 1
        self.tree = [Node(0)] * self.tree_size
        self._build_tree(0, self.start, self.end)


    def query(self, start, end):
        """
        Query the range [start, end]
        """
        return self._query(0, self.start, self.end, start, end).val


    def update(self, start, end, value):
        """
        Increment the numbers in the range [start, end]
        by value.
        """
        self._update(0, self.start, self.end, start, end, value)
        pass


    def _build_tree(self, root_idx, start, end):
        """
        Utility function to construct the segment tree.
        """
        if start > end:
            return

        # Leaf node
        if start == end:
            self.tree[root_idx] = Node(self.arr[start])
            return

        mid = (start + end) / 2
        # Initialize the left child
        self._build_tree(root_idx*2+1, start, mid)
        # Initialize the right child
        self._build_tree(root_idx*2+2, mid+1, end)

        self.tree[root_idx] = merge(self.tree[root_idx*2+1], self.tree[root_idx*2+2])


    def _query(self, root_idx, left_most_leaf, right_most_leaf, start, end):
        """
        Utility method that actually does the query.
        Returns the node containing the answer.
        """
        if start > right_most_leaf or end < left_most_leaf:
            return

        # If the current segment is totally within the range [start, end]
        if left_most_leaf >= start and right_most_leaf <= end:
            return self.tree[root_idx]

        mid = (left_most_leaf + right_most_leaf) / 2

        q_left = self._query(root_idx*2+1, left_most_leaf, mid, start, end)
        q_right = self._query(root_idx*2+2, mid+1, right_most_leaf, start, end)

        return merge(q_left, q_right)


    def _update(self, root_idx, left_most_leaf, right_most_leaf, start, end, value):
        """
        Utility method that actually performs the update.
        """
        if start > right_most_leaf or end < left_most_leaf or start > end:
            # Out of range
            return
        if left_most_leaf == right_most_leaf:
            self.tree[root_idx].val += value
            return

        mid = (left_most_leaf + right_most_leaf) / 2
        self._update(root_idx*2+1, left_most_leaf, mid, start, end, value)
        self._update(root_idx*2+2, mid+1, right_most_leaf, start, end, value)

        self.tree[root_idx] = merge(self.tree[root_idx*2+1],
                self.tree[root_idx*2+2])

    def print_tree(self):
        for root_idx, node in enumerate(self.tree):
            print str(root_idx) + ": " + str(self.tree[root_idx].val)


a = [1, 3, 2, 6, 4]
seg_tree = SegmentTree(a)
print seg_tree.query(0,1)
print seg_tree.query(0,3)
print seg_tree.query(0,4)
print seg_tree.query(1,2)


