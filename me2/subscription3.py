from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
# subscription = {
#     "customer": "C1",
#     "history": [
#         {"plan": "BASIC", "start": "2025-01-15", "end": "2025-03-31", "trial_days": 10},
#         {"plan": "PREMIUM", "start": "2025-04-01", "end": None}
#     ]
# }
d=  "2025-01-15"
# print(datetime.strptime(d, "%Y-%m-%d") if d else None)
# 2025-01-15 00:00:00

PLANS = {
    "BASIC": 9.99,
    "STANDARD": 49.99,
    "PREMIUM": 249.99
}

def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d") if d else None

def month_range(dt):
    """Return first and last day of the month of the given date"""
    first_day = dt.replace(day=1)
    last_day = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
    return first_day, last_day

def days_overlap(start1, end1, start2, end2):
    """Calculate the number of overlapping days between two date ranges"""
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    delta = (earliest_end - latest_start).days + 1
    return max(0, delta)

def generate_cost_report(subscription, year):
    plan_periods = []

    for entry in subscription["history"]:
        start = parse_date(entry["start"])
        end = parse_date(entry["end"]) or datetime(year, 12, 31)
        plan = entry["plan"]
        trial_days = entry.get("trial_days", 0)
        trial_end = start + timedelta(days=trial_days)
        plan_periods.append((start, end, trial_end, plan))

    monthly_costs = {}
    total_cost = 0
    current = datetime(year, 1, 1)
    end_of_year = datetime(year, 12, 31)

    while current <= end_of_year:
        month_start, month_end = month_range(current)
        month_key = current.strftime("%Y-%m")
        cost = 0.0
        plan_for_month = "NONE"

        for start, end, trial_end, plan in plan_periods:
            overlap_days = days_overlap(month_start, month_end, start, end)
            if overlap_days == 0:
                continue

            # Calculate trial overlap and billable days
            trial_overlap = days_overlap(month_start, month_end, start, \
             trial_end - timedelta(days=1))
            billable_days = overlap_days - trial_overlap

            if billable_days > 0:
                total_days = (month_end - month_start).days + 1
                prorated_cost = (billable_days / total_days) * PLANS[plan]
                cost += prorated_cost
                plan_for_month = plan if trial_overlap == 0 else f"{plan} \
                (partial w/ trial)"
            elif trial_overlap > 0:
                plan_for_month = f"{plan} (trial)"
                cost += 0.0

        monthly_costs[month_key] = {
            "plan": plan_for_month,
            "cost": round(cost, 2)
        }
        total_cost += cost
        current += relativedelta(months=1)

    return {
        "monthly_breakdown": monthly_costs,
        "yearly_total": round(total_cost, 2)
    }
