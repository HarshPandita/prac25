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

class WeekdayRule:
    def __init__(self, allowed_days):
        """
        allowed_days: list of int (0=Monday, 6=Sunday)
        """
        self.allowed_days = allowed_days

    def apply(self, expense):
        date_str = expense.get("date")
        if not date_str:
            return "Expense must include a 'date' field"

        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return f"Invalid date format for expense: {date_str} (expected YYYY-MM-DD)"

        weekday = date_obj.weekday()
        if weekday not in self.allowed_days:
            weekday_name = date_obj.strftime("%A")
            return f"Expenses not allowed on {weekday_name}s"



class RuleEngine:
    def __init__(self, rule_list):
        self.rule_list = rule_list

    def apply(self, expense_list):
        results = []
        
        for expense in expense_list:
            errors = []
            for rule in self.rule_list:
                err = rule.apply(expense)
                if err:
                    errors.append(err)
            if errors:
                results.append({
                    "expense": expense,
                    "errors": errors
                })
            
        return results if results else "All txns approved"


# === Instantiate rules ===
rule1 = AllowedExpenseType(["seller", "vendor"])
rule2 = TotalExpense(250)
rule3 = ExpenseTypeRule({"seller": 100, "vendor": 200})
weekday_rule = WeekdayRule([0, 1, 2, 3, 4])


engine = RuleEngine([rule1, rule2, rule3,weekday_rule])

# === Sample input ===
expenses = [
    {"type": "seller", "amount": 50, "date": "2025-06-23"},      # Monday - OK
    {"type": "vendor", "amount": 300, "date": "2025-06-22"},     # Sunday - disallowed
    {"type": "contractor", "amount": 100, "date": "2025-06-21"}, # Saturday - disallowed + type not allowed
    {"type": "seller", "amount": 120, "date": "2025-06-25"},     # Wednesday - OK but seller > 100
]
# === Run engine ===
result = engine.apply(expenses)
print(result)