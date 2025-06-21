class Node:
    def __init__(self, count):
        self.count = count
        self.keys = set()
        self.prev = self.next = None

class AllOne:

    def __init__(self):
        self.head = Node(float('-inf'))
        self.tail = Node(float('inf'))
        self.head.next = self.tail
        self.tail.prev = self.head

        self.key_node = dict()  # key -> Node
        self.most_recent_map = dict()  # count -> most recently incremented key

    def _insert_after(self, node, new_node):
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def inc(self, key: str) -> None:
        if key in self.key_node:
            node = self.key_node[key]
            next_node = node.next
            if next_node.count != node.count + 1:
                new_node = Node(node.count + 1)
                self._insert_after(node, new_node)
            else:
                new_node = next_node
            new_node.keys.add(key)
            self.key_node[key] = new_node

            node.keys.remove(key)
            if not node.keys:
                self._remove(node)

            self.most_recent_map[new_node.count] = key  # update recent
        else:
            # New key
            next_node = self.head.next
            if next_node.count != 1:
                new_node = Node(1)
                self._insert_after(self.head, new_node)
            else:
                new_node = next_node
            new_node.keys.add(key)
            self.key_node[key] = new_node
            self.most_recent_map[1] = key  # update recent

    def dec(self, key: str) -> None:
        if key not in self.key_node:
            return

        node = self.key_node[key]
        if node.count == 1:
            del self.key_node[key]
        else:
            prev_node = node.prev
            if prev_node.count != node.count - 1:
                new_node = Node(node.count - 1)
                self._insert_after(prev_node, new_node)
            else:
                new_node = prev_node
            new_node.keys.add(key)
            self.key_node[key] = new_node
            self.most_recent_map[new_node.count] = key  # update recent

        node.keys.remove(key)
        if not node.keys:
            self._remove(node)

    def getMaxKey(self) -> str:
        if self.tail.prev == self.head:
            return ""
        max_count = self.tail.prev.count
        return self.most_recent_map.get(max_count, "")

    def getMinKey(self) -> str:
        if self.head.next == self.tail:
            return ""
        return next(iter(self.head.next.keys))
