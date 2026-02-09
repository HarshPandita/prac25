from collections import defaultdict

class Context:
    def __init__(self):
        self.trip_totals = defaultdict(float)
        self.trip_type_totals = defaultdict(float)

class BanRule:
    def __init__(self, field, value, name):
        self.field = field
        self.value = value
        self.name = name

    def evaluate(self, expense, context):
        if expense.get(self.field) == self.value:
            return "expense"


class MaxExpenseRule:
    def __init__(self, limit):
        self.limit = limit
        self.name = "max_expense"

    def evaluate(self, expense, context):
        if float(expense["amount_usd"]) > self.limit:
            return "expense"


class VendorTypeLimitRule:
    def __init__(self, vendor_type, limit):
        self.vendor_type = vendor_type
        self.limit = limit
        self.name = "vendor_limit"

    def evaluate(self, expense, context):
        if expense["vendor_type"] == self.vendor_type:
            if float(expense["amount_usd"]) > self.limit:
                return "expense"


class TripTotalRule:
    def __init__(self, limit):
        self.limit = limit
        self.name = "trip_total_limit"

    def evaluate(self, expense, context):
        trip_id = expense["trip_id"]
        if context.trip_totals[trip_id] > self.limit:
            return "trip"


class ExpenseTypeAggregationRule:
    def __init__(self, expense_type, limit):
        self.expense_type = expense_type
        self.limit = limit
        self.name = "type_total_limit"

    def evaluate(self, expense, context):
        if expense["expense_type"] == self.expense_type:
            key = (expense["trip_id"], expense["expense_type"])
            if context.trip_type_totals[key] > self.limit:
                return "trip"

def evaluateRules(rules, expenses):

    result = {
        "expense_violations": defaultdict(list),
        "trip_violations": defaultdict(list)
    }

    context = Context()

    for expense in expenses:
        expense_id = expense["expense_id"]
        trip_id = expense["trip_id"]
        amount = float(expense["amount_usd"])

        # Update aggregations
        context.trip_totals[trip_id] += amount
        key = (trip_id, expense["expense_type"])
        context.trip_type_totals[key] += amount

        # Apply rules
        for rule in rules:
            level = rule.evaluate(expense, context)

            if level == "expense":
                result["expense_violations"][expense_id].append(rule.name)

            elif level == "trip":
                result["trip_violations"][trip_id].append(rule.name)

    return result


def test_basic_rules():
    rules = [
        VendorTypeLimitRule("restaurant", 75),
        BanRule("expense_type", "airfare", "Airfare expenses are not allowed"),
        BanRule("expense_type", "entertainment",
                "Entertainment expenses are not allowed"),
        MaxExpenseRule(250),
        TripTotalRule(2000),
        ExpenseTypeAggregationRule("meal", 200),
    ]

    expenses = [
        {
            "expense_id": "001",
            "trip_id": "T1",
            "amount_usd": "50",
            "expense_type": "meal",
            "vendor_type": "restaurant",
            "vendor_name": "Outback"
        },
        {
            "expense_id": "002",
            "trip_id": "T1",
            "amount_usd": "300",
            "expense_type": "hotel",
            "vendor_type": "hotel",
            "vendor_name": "Hilton"
        },
        {
            "expense_id": "003",
            "trip_id": "T1",
            "amount_usd": "100",
            "expense_type": "airfare",
            "vendor_type": "airline",
            "vendor_name": "Delta"
        }
    ]

    result = evaluateRules(rules, expenses)
    print("Basic Test Result:")
    print(result)

test_basic_rules()