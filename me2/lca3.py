# O(n)

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def lowestCommonAncestor(root: TreeNode, nodes: list[TreeNode]) -> TreeNode:
    node_set = set(nodes)  # Fast lookup
    result = [None]

    def dfs(node):
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)
        mid = 1 if node in node_set else 0

        total = left + right + mid

        if total == len(nodes) and result[0] is None:
            result[0] = node

        return total

    dfs(root)
    return result[0]
