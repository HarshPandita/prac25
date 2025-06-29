from collections import defaultdict, deque
# | Method                    | Time Complexity      | Explanation                                                                                    |
# | ------------------------- | -------------------- | ---------------------------------------------------------------------------------------------- |
# | `set(cell, value)`        | **O(d + R × d × T)** | - `d`: extract dependencies from formula<br>- `R × d × T`: propagate recomputes for dependents |
# | `reset(cell)`             | **O(R × d × T)**     | Same as `set`, but skips parsing dependencies (only recomputes affected cells)                 |
# | `get_value(cell)`         | **O(D × T)**         | - Recursive traversal of formula references<br>- T = tokens per formula                        |
# | `_recompute(cell)`        | **O(R)**             | - BFS through reverse dependency graph<br>- Clears `R` cached values                           |
# | `_extract_deps()`         | **O(L)**             | L = length of formula string (linear scan)                                                     |
# | `_parse_formula()`        | **O(L)**             | Split and normalize `+/-` manually                                                             |
# | `_rebuild_reverse_deps()` | **O(n × d)**         | For each formula, iterate through its `d` dependencies                                         |

class Excel:
    def __init__(self):
        self.values = {}               # A1 -> 10
        self.formulas = {}             # A1 -> "=B1+2"
        self.dependencies = {}         # A1 -> [B1]
        self.reverse_dependencies = defaultdict(set)  # B1 -> {A1}
    def set(self, cell, value):
        if value.startswith('='):
            self.formulas[cell] = value
            deps = self._extract_deps(value[1:])
            self.dependencies[cell] = deps
            self.values.pop(cell, None)  # Remove old value
        else:
            self.values[cell] = int(value)
            self.formulas.pop(cell, None)
            self.dependencies.pop(cell, None)
        self._rebuild_reverse_deps()
        self._recompute(cell)
    def reset(self, cell):
        self.values.pop(cell, None)
        self.formulas.pop(cell, None)
        for dep in self.dependencies.get(cell, []):
            self.reverse_dependencies[dep].discard(cell)
        self.dependencies.pop(cell, None)
        self._recompute(cell)
    def get_value(self, cell):
        return self._eval(cell, set())
    def print(self):
        all_cells = set(self.values.keys()) | set(self.formulas.keys()) | set(self.dependencies.keys())
        for cell in sorted(all_cells):
            raw = self.formulas.get(cell, str(self.values.get(cell, '')))
            val = self.get_value(cell)
            print(f"{cell}: raw={raw}, value={val}")
    def _extract_deps(self, formula):
        tokens = formula.replace('-', '+-').split('+')
        deps = []
        for token in tokens:
            token = token.strip()
            if token and not token.lstrip('-').isdigit():
                deps.append(token.lstrip('-'))
        return deps
    def _eval(self, cell, visited):
        if cell in visited:
            return -1  # cycle
        if cell in self.values:
            return self.values[cell]
        if cell not in self.formulas:
            return 0
        visited.add(cell)
        tokens = self.formulas[cell][1:].replace('-', '+-').split('+')
        total = 0
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token.lstrip('-').isdigit():
                total += int(token)
            else:
                sign = -1 if token.startswith('-') else 1
                ref = token[1:] if sign == -1 else token
                val = self._eval(ref, visited)
                if val == -1:
                    return -1
                total += sign * val
        visited.remove(cell)
        self.values[cell] = total  # cache
        return total
    def _rebuild_reverse_deps(self):
        self.reverse_dependencies.clear()
        for cell, deps in self.dependencies.items():
            for dep in deps:
                self.reverse_dependencies[dep].add(cell)
    def _recompute(self, start_cell):
        visited = set()
        queue = deque([start_cell])
        while queue:
            curr = queue.popleft()
            for dependent in self.reverse_dependencies.get(curr, []):
                if dependent not in visited:
                    visited.add(dependent)
                    self.values.pop(dependent, None)  # force re-eval
                    queue.append(dependent)
xl = Excel()
xl.set("A1", "5")
xl.set("B1", "3")
xl.set("C1", "=A1+B1+2")
xl.set("D1", "=C1+A1")
xl.print()

print("\n-- update A1 to 10 --")
xl.set("A1", "10")
xl.print()

print("\n-- reset A1 --")
xl.reset("A1")
xl.print()

print("\n-- cycle test --")
xl.set("X1", "=Y1+1")
xl.set("Y1", "=X1+1")
xl.print()