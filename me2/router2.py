class TrieNode:
    def __init__(self):
        self.val = -1
        self.children = {}

class FileSystem:
    def __init__(self):
        self.root = TrieNode()

    def put(self, path, value):
        # Split and remove empty parts (to handle "//" and leading/trailing slashes)
        parts = [part for part in path.split("/") if part]
        node = self.root

        for part in parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]

        node.val = value
        return True

    def get(self, path):
        parts = [part for part in path.split("/") if part]
        return self._get_helper(self.root, parts, 0)

    def _get_helper(self, node, parts, index):
        if index == len(parts):
            return node.val

        part = parts[index]
        if part == "*":
            # Wildcard: try all children
            for child in node.children.values():
                result = self._get_helper(child, parts, index + 1)
                if result != -1:
                    return result
            return -1

        if part in node.children:
            return self._get_helper(node.children[part], parts, index + 1)

        return -1
