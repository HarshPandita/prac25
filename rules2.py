import datetime
from collections import defaultdict

class BaseRule:
    def apply(self, grouped_expenses):
        raise NotImplementedError

class AllowedExpenseType(BaseRule):
    def __init__(self, allowed_types):
        self.allowed_types = set(allowed_types)

    def apply(self, grouped_expenses):
        results = []
        for trip_id, expenses in grouped_expenses.items():
            errors = []
            for expense in expenses:
                if expense["type"] not in self.allowed_types:
                    errors.append(f"'{expense['type']}' is not allowed in trip {trip_id}")
            if errors:
                results.append((trip_id, errors))
        return results

class ExpenseTypeRule(BaseRule):
    def __init__(self, rule_map):
        self.rule_map = rule_map  # e.g., {"seller": 100, "vendor": 200}

    def apply(self, grouped_expenses):
        results = []
        for trip_id, expenses in grouped_expenses.items():
            type_totals = defaultdict(int)
            for e in expenses:
                type_totals[e["type"]] += e["amount"]

            errors = []
            for t, max_allowed in self.rule_map.items():
                if type_totals[t] > max_allowed:
                    errors.append(
                        f"Total expense of type '{t}' in trip {trip_id} is {type_totals[t]} which exceeds limit {max_allowed}"
                    )
            if errors:
                results.append((trip_id, errors))
        return results

class TotalExpense(BaseRule):
    def __init__(self, limit):
        self.limit = limit

    def apply(self, grouped_expenses):
        results = []
        for trip_id, expenses in grouped_expenses.items():
            total = sum(e["amount"] for e in expenses)
            if total > self.limit:
                results.append((trip_id, [f"Trip {trip_id} total {total} exceeds limit {self.limit}"]))
        return results

class WeekdayRule(BaseRule):
    def __init__(self, allowed_days):
        self.allowed_days = set(allowed_days)

    def apply(self, grouped_expenses):
        results = []
        for trip_id, expenses in grouped_expenses.items():
            errors = []
            for e in expenses:
                date_str = e.get("date")
                if not date_str:
                    errors.append("Missing date field")
                    continue
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    errors.append(f"Invalid date format: {date_str} (expected YYYY-MM-DD)")
                    continue

                if date_obj.weekday() not in self.allowed_days:
                    errors.append(f"Trip {trip_id}: Expenses not allowed on {date_obj.strftime('%A')}")
            if errors:
                results.append((trip_id, errors))
        return results

class ConditionalTypeCapRule(BaseRule):
    def __init__(self, total_threshold, conditional_caps):
        self.total_threshold = total_threshold              # e.g., 400
        self.conditional_caps = conditional_caps            # e.g., {"food": 50}

    def apply(self, grouped_expenses):
        results = []
        for trip_id, expenses in grouped_expenses.items():
            total = sum(e["amount"] for e in expenses)
            if total <= self.total_threshold:
                continue

            type_totals = defaultdict(int)
            for e in expenses:
                t = e["type"]
                if t in self.conditional_caps:
                    type_totals[t] += e["amount"]

            errors = []
            for t, limit in self.conditional_caps.items():
                if type_totals[t] > limit:
                    errors.append(
                        f"Trip {trip_id}: {t} total {type_totals[t]} exceeds cap {limit} (applied because total {total} > {self.total_threshold})"
                    )

            if errors:
                results.append((trip_id, errors))

        return results

class AndRule(BaseRule):
    def __init__(self, *rules):
        self.rules = rules

    def apply(self, grouped_expenses):
        all_results = []
        for rule in self.rules:
            all_results.extend(rule.apply(grouped_expenses))
        return all_results


class OrRule(BaseRule):
    def __init__(self, *rules):
        self.rules = rules

    def apply(self, grouped_expenses):
        errors_by_trip = defaultdict(list)
        for rule in self.rules:
            for trip_id, errors in rule.apply(grouped_expenses):
                errors_by_trip[trip_id].append(errors)

        final = []
        for trip_id, all_errs in errors_by_trip.items():
            if all(all_errs):  # all failed
                flat = [e for err_list in all_errs for e in err_list]
                final.append((trip_id, flat))
        return final

class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def apply(self, expense_list):
        grouped = defaultdict(list)
        for exp in expense_list:
            grouped[exp.get("trip_id", "UNKNOWN")].append(exp)

        error_map = defaultdict(list)
        for rule in self.rules:
            for trip_id, errs in rule.apply(grouped):
                error_map[trip_id].extend(errs)

        if not error_map:
            return "All trips approved"

        return [
            {"trip_id": tid, "errors": errs}
            for tid, errs in error_map.items()
        ]
def evaluate_rules(rules, expenses):
    engine = RuleEngine(rules)
    return engine.apply(expenses)

from pprint import pprint

rules = [
    AndRule(
        AllowedExpenseType(["seller", "vendor", "food"]),
        ExpenseTypeRule({"seller": 100, "vendor": 200, "food": 100})
        # TotalExpense(500),
        # WeekdayRule([0, 1, 2, 3, 4]),
        # ConditionalTypeCapRule(400, {"food": 50})
    )
]
expenses = [
        {"trip_id": "T1", "type": "seller", "amount": 50, "date": "2025-06-23"},
        {"trip_id": "T1", "type": "vendor", "amount": 300, "date": "2025-06-22"},
        {"trip_id": "T2", "type": "contractor", "amount": 100, "date": "2025-06-21"},
        {"trip_id": "T1", "type": "seller", "amount": 120, "date": "2025-06-25"},
        {"trip_id": "T1", "type": "food", "amount": 60, "date": "2025-06-25"},
    ]
pprint(evaluate_rules(rules, expenses))