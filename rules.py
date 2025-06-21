class CatRule:
    def __init__(self, allowed_catargories):
        self.allowed_cats = allowed_catargories

    def apply(self, expense):
        if expense["category"] not in  self.allowed_cats:
            return({"bad":True,"desc":f'{expense["category"]} - is not an allowed cataegory'})
        else:
            return({"bad":False})

class ExpRule:
    def __init__(self, limits):
        self.limits = limits

    def apply(self, expense):
        if expense["category"] in self.limits and expense["amount"] > self.limits[expense["category"]]:
            return({"bad":True,"desc":f'{expense["amount"]} - is greater then the limit of {expense["category"]}'})
        
        else:
            return({"bad":False})


class RulesEngine:
    def __init__(self, rules):
        self.rules = rules
        
    def validate_expenses(self, expenses):
        errors = []
        for exp in expenses:
            for rule in self.rules:
                if rule.apply(exp)["bad"]:
                    errors.append(rule.apply(exp)["desc"])

        print(errors)
    

rules = [
    CatRule(["Travel", "Food", "Lodging"]),
    ExpRule({"Travel": 300, "Food": 100})
]

engine = RulesEngine(rules)

expenses = [
    {"employee_id": "E001", "date": "2025-06-06", "category": "123", "amount": 350, "description": "Flight"},
    {"employee_id": "E002", "date": "2025-06-01", "category": "Food", "amount": 888, "description": "Dinner"}
    ]

engine.validate_expenses(expenses)


# 
class ExpenseTypeRule:
    def __init__(self, rule_map):
        self.rule_map = rule_map  # e.g., {"seller": 100, "vendor": 200}

    def apply(self, expense):
        exp_type = expense["type"]
        if exp_type in self.rule_map and expense["amount"] > self.rule_map[exp_type]:
            return f"Seller type '{exp_type}' should not have expense more than {self.rule_map[exp_type]}"


class TotalExpense:
    def __init__(self, limit):
        self.limit = limit

    def apply(self, expense):
        if expense["amount"] > self.limit:
            return f"Total expense should not be > {self.limit}"


class AllowedExpenseType:
    def __init__(self, allowed_types):
        self.allowed_types = allowed_types

    def apply(self, expense):
        if expense["type"] not in self.allowed_types:
            return f"'{expense['type']}' type should not be charged"


class RuleEngine:
    def __init__(self, rule_list):
        self.rule_list = rule_list

    def apply(self, expense_list):
        errors = []
        for expense in expense_list:
            for rule in self.rule_list:
                err = rule.apply(expense)
                if err:
                    errors.append(err)
        return errors if errors else "All txns approved"


# === Instantiate rules ===
rule1 = AllowedExpenseType(["seller", "vendor"])
rule2 = TotalExpense(250)
rule3 = ExpenseTypeRule({"seller": 100, "vendor": 200})

engine = RuleEngine([rule1, rule2, rule3])

# === Sample input ===
expenses = [
    {"type": "seller", "amount": 50},       # OK
    {"type": "vendor", "amount": 300},      # Total > 250 and vendor limit = 200
    {"type": "contractor", "amount": 100},  # Not allowed type
    {"type": "seller", "amount": 120},      # Seller exceeds type limit
]

# === Run engine ===
result = engine.apply(expenses)
print(result)