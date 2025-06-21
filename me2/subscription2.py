from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

PLANS = {
    "BASIC": 9.99,
    "STANDARD": 49.99,
    "PREMIUM": 249.99
}

def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d") if d else None

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
        plan_for_month = None
        cost = 0.0

        for start, end, trial_end, plan in plan_periods:
            if start <= current <= end:
                if current < trial_end:
                    plan_for_month = f"{plan} (trial)"
                    cost = 0.0
                else:
                    plan_for_month = plan
                    cost = PLANS[plan]
                break

        month_key = current.strftime("%Y-%m")
        if plan_for_month:
            monthly_costs[month_key] = {"plan": plan_for_month, "cost": cost}
            total_cost += cost
        else:
            monthly_costs[month_key] = {"plan": "NONE", "cost": 0.0}

        current += relativedelta(months=1)

    return {
        "monthly_breakdown": monthly_costs,
        "yearly_total": round(total_cost, 2)
    }
