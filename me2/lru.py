class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node

        # Dummy head and tail to avoid edge checks
        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        # Remove an existing node from the linked list
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_front(self, node: Node):
        # Always add new node right after head
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self._add_to_front(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            # Remove from the tail
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
