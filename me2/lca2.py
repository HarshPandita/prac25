class Node:
    def __init__(self, name, node_type):
        self.name = name
        self.type = node_type  # 'Company', 'Department', 'Employee'
        self.children = []

    def __repr__(self):
        return f"{self.type}({self.name})"


def find_lca(root, p, q):
    """
    Returns the lowest common ancestor (department or company) of nodes p and q.
    """
    if not root:
        return None

    if root == p or root == q:
        return root

    matches = []

    for child in root.children:
        res = find_lca(child, p, q)
        if res:
            matches.append(res)

    if len(matches) >= 2:
        return root

    return matches[0] if matches else None


# === Example Setup ===

# Build the hierarchy
company = Node("MyCompany", "Company")

deptA = Node("DeptA", "Department")
deptB = Node("DeptB", "Department")
subDeptA1 = Node("SubDeptA1", "Department")

emp1 = Node("Alice", "Employee")
emp2 = Node("Bob", "Employee")
emp3 = Node("Charlie", "Employee")

# Tree construction
company.children = [deptA, deptB]
deptA.children = [subDeptA1]
subDeptA1.children = [emp1, emp2]
deptB.children = [emp3]

# === Example Usage ===

# LCA of emp1 and emp2 → SubDeptA1
lca1 = find_lca(company, emp1, emp2)
print("LCA of emp1 and emp2:", lca1)

# LCA of emp1 and emp3 → Company
lca2 = find_lca(company, emp1, emp3)
print("LCA of emp1 and emp3:", lca2)

# LCA of emp1 and subDeptA1 → SubDeptA1
lca3 = find_lca(company, emp1, subDeptA1)
print("LCA of emp1 and subDeptA1:", lca3)
