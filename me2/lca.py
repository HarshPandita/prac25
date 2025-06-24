class Node:
    def __init__(self, name, node_type):
        self.name = name
        self.type = node_type  # 'Company', 'Department', or 'Employee'
        self.children = []
        self.parent = None

    def __repr__(self):
        return f"{self.type}: {self.name}"

# O(E*H)
def build_hierarchy():
    # Sample tree
    company = Node("Company", "Company")

    deptA = Node("DeptA", "Department")
    empX = Node("X", "Employee")
    empY = Node("Y", "Employee")
    deptA.children = [empX, empY]
    empX.parent = empY.parent = deptA

    deptB = Node("DeptB", "Department")
    empZ = Node("Z", "Employee")
    deptB.children = [empZ]
    empZ.parent = deptB

    company.children = [deptA, deptB]
    deptA.parent = deptB.parent = company

    # Build name lookup
    name_to_node = {n.name: n for n in [company, deptA, deptB, empX, empY, empZ]}

    return company, name_to_node


def get_path_to_root(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]  # From root to leaf


def find_closest_common_department(employee_names, name_to_node):
    paths = [get_path_to_root(name_to_node[name]) for name in employee_names]

    min_len = min(len(p) for p in paths)
    lca = None
    for i in range(min_len):
        if all(path[i] == paths[0][i] for path in paths):
            if paths[0][i].type == "Department":
                lca = paths[0][i]
        else:
            break
    return lca


# -------------------------------
# Example usage
company, name_to_node = build_hierarchy()
employees = ["X", "Y"]  # Try ["X", "Z"] for DeptA vs DeptB
lca = find_closest_common_department(employees, name_to_node)
print("Closest common department:", lca)
