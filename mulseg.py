from math import log, ceil
# Implementation of Segment Trees in Python
# No Lazy Propogation

def merge(left_node, right_node):
    """
    Returns the node obtained by merging
    left_node and right_node
    """
    merged_node = Node(1,0)
    if not left_node:
        left_node = Node(1,0)
    if not right_node:
        right_node = Node(1,0)
    merged_node.val = (left_node.val * right_node.val) % K
    merged_node.length = left_node.length + right_node.length
    return merged_node


class Node(object):
    """
    A segment tree node.
    """

    def __init__(self, val=1, length=1):
        self.val = val
        self.length = length

class SegmentTree(object):
    """
    A segment tree
    """

    def __init__(self, arr):
        self.arr = arr
        self.start = 0
        self.end = len(arr)-1
        self.tree_size = int(2 * (2 ** ceil(log(len(arr),2))) - 1)
        self.tree = [Node(1,0)] * self.tree_size
        self.possible_interval = 0
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


    def _build_tree(self, root_idx, start, end):
        """
        Utility function to construct the segment tree.
        """
        if start > end:
            return

        # Leaf node
        if start == end:
            self.tree[root_idx] = Node(self.arr[start] % K, 1)
            if self.tree[root_idx].val == 0:
                self.possible_interval = 1
            return

        mid = (start + end) / 2
        # Initialize the left child
        self._build_tree(root_idx*2+1, start, mid)
        # Initialize the right child
        self._build_tree(root_idx*2+2, mid+1, end)

        self.tree[root_idx] = merge(self.tree[root_idx*2+1], self.tree[root_idx*2+2])
        if self.tree[root_idx].val == 0:
            if self.possible_interval ==0:
                self.possible_interval = end - start + 1


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
        """
        Print the segment tree in the fashion
        index: value
        """
        for root_idx, node in enumerate(self.tree):
            print str(root_idx) + ": " + str(self.tree[root_idx].val)


K, N = map(int, raw_input().split())
a = [int(x) for x in raw_input().split()]
seg_tree = SegmentTree(a)
if seg_tree.possible_interval == 0:
    print 'NONE'

else:
    print 'Minimum interval length: ' + str(seg_tree.possible_interval)
    found_intervals = []
    product = 1
    for i in xrange(0,seg_tree.possible_interval):
        product = product * a[i]

    for i in xrange(0, len(a)-seg_tree.possible_interval+1):
        if product % K == 0:
            found_intervals.append((i+1, i+1+seg_tree.possible_interval-1))
        product = product / a[i]
        if i != len(a)-seg_tree.possible_interval:
            product = product * a[i+seg_tree.possible_interval]
    found_intervals.sort()
    print 'Found intervals:'
    for item in found_intervals:
        print '[' + str(item[0]) + ', ' + str(item[1]) + ']'



