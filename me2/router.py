class TrieNode:
    def __init__(self):
        self.val = -1
        self.children = {}
    

class FileSystem:
    def __init__(self):
        self.root = TrieNode()

    def put(self, path, value):
        path_list = path.split("/")
        node = self.root
        for i in range(len(path_list)):
            curr_part  = path_list[i]
            if i == len(path_list) -1:
                if curr_part in node.children:
                    node.children[curr_part].val = value
                    return True
                node.children[curr_part] = TrieNode()
                node.children[curr_part].val = value
                return True

            else:
                if curr_part not in node.children:
                    print("here")
                    self.put(curr_part,0)
                    # return False
                node = node.children[curr_part]
        return False

    def get(self, path):
        path_list = path.split("/")
        return self.helper(self.root, path_list,0)
    def helper(self, node, parts, index):
        if index == len(parts):
            return node.val
        
        part = parts[index]
        if part == "*":
            for child in node.children.values():
                result = self.helper(child, parts, index+1)
                if result!=-1:
                    return result
            return -1
        
        if part in node.children:
            return self.helper(node.children[part], parts, index+1)
        
        return -1
fs = FileSystem()
# fs.put("a","a")
fs.put("a/b","b")
fs.put("a/b/c","c")
print(fs.get("a/*"))