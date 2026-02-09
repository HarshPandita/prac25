from collections import defaultdict
from datetime import datetime
class Context:
    def __init__(self):
        self.trip_totals = defaultdict(float)
        self.trip_type_totals = defaultdict(float)

class BanRule:
    def __init__(self, field, value, message):
        self.field = field #expense_type/vendor_type
        self.value = value #meal/restaurant
        self.message = message

    def evaluate(self, expense, context):
        if expense.get(self.field) == self.value:
            return {
                "level": "expense",
                "rule": "ban_rule",
                "message": self.message
            }


class MaxExpenseRule:
    def __init__(self, limit):
        self.limit = limit

    def evaluate(self, expense, context):
        amount = float(expense["amount_usd"])
        if amount > self.limit:
            return {
                "level": "expense",
                "rule": "max_expense",
                "message": "Expense cannot exceed $" + str(self.limit),
                "actual": amount,
                "limit": self.limit
            }


class VendorTypeLimitRule:
    def __init__(self, vendor_type, limit):
        self.vendor_type = vendor_type
        self.limit = limit

    def evaluate(self, expense, context):
        if expense["vendor_type"] == self.vendor_type:
            amount = float(expense["amount_usd"])
            if amount > self.limit:
                return {
                    "level": "expense",
                    "rule": "vendor_limit",
                    "message": self.vendor_type +
                               " expense cannot exceed $" + str(self.limit),
                    "actual": amount,
                    "limit": self.limit
                }


class TripTotalRule:
    def __init__(self, limit):
        self.limit = limit

    def evaluate(self, expense, context):
        trip_id = expense["trip_id"]
        total = context.trip_totals[trip_id]
        if total > self.limit:
            return {
                "level": "trip",
                "rule": "trip_total_limit",
                "message": "Trip total exceeded $" + str(self.limit),
                "total": total,
                "limit": self.limit
            }


class ExpenseTypeAggregationRule:
    def __init__(self, expense_type, limit):
        self.expense_type = expense_type
        self.limit = limit

    def evaluate(self, expense, context):
        if expense["expense_type"] == self.expense_type:
            key = (expense["trip_id"], expense["expense_type"])
            total = context.trip_type_totals[key]

            if total > self.limit:
                return {
                    "level": "trip",
                    "rule": "type_total_limit",
                    "message": self.expense_type +
                               " expenses exceeded $" + str(self.limit),
                    "total": total,
                    "limit": self.limit
                }

class WeekdayRule:
    """
    allowed_days example:
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    Useful to ban weekends.
    """

    def __init__(self, allowed_days):
        self.allowed_days = allowed_days

    def evaluate(self, expense, context):
        date_str = expense.get("date")
        if not date_str:
            return

        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day = dt.strftime("%A")

        if day not in self.allowed_days:
            return {
                "level": "expense",
                "rule": "weekday_rule",
                "message": "Expenses not allowed on " + day
            }

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

        # ---- update aggregations ----
        context.trip_totals[trip_id] += amount

        key = (trip_id, expense["expense_type"])
        context.trip_type_totals[key] += amount

        # ---- evaluate rules ----
        for rule in rules:
            violation = rule.evaluate(expense, context)

            if violation:
                if violation["level"] == "expense":
                    result["expense_violations"][expense_id].append(violation)
                else:
                    result["trip_violations"][trip_id].append(violation)

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
    WeekdayRule(["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday"])
    ]

    expenses = [
        {
            "expense_id": "001",
            "trip_id": "T1",
            "amount_usd": "50",
            "expense_type": "meal",
            "vendor_type": "restaurant",
            "vendor_name": "Outback",
            "date": "2025-02-07"
        },
        {
            "expense_id": "002",
            "trip_id": "T1",
            "amount_usd": "300",
            "expense_type": "hotel",
            "vendor_type": "hotel",
            "vendor_name": "Hilton",
            "date": "2025-02-08"
        },
        {
            "expense_id": "003",
            "trip_id": "T1",
            "amount_usd": "100",
            "expense_type": "airfare",
            "vendor_type": "airline",
            "vendor_name": "Delta",
            "date": "2025-02-07"
        }
    ]

    result = evaluateRules(rules, expenses)
    print("Basic Test Result:")
    print(result)

test_basic_rules()