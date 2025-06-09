class Excel:
    def __init__(self):
        self.cells = {}

    def set(self, cell, value):
        self.cells[cell] = value

    def get_value(self, cell, visited=None):
        if visited is None:
            visited = set()
        if cell in visited:
            return -1  # cycle detected
        visited.add(cell)

        value = self.cells.get(cell, "")
        if not value.startswith("="):
            return int(value) if value else 0

        expr = value[1:]  # remove '='
        tokens = expr.replace('-', '+-').split('+')
        total = 0

        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                total += int(token)
            else:
                val = self.get_value(token, visited.copy())
                if val == -1:
                    return -1
                total += val

        return total

    def print(self):
        for cell in sorted(self.cells):
            raw = self.cells[cell]
            computed = self.get_value(cell)
            print(f"{cell}: raw = {raw}, computed = {computed}")
