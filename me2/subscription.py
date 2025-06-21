from datetime import datetime, timedelta
import calendar

PRICING = {
    'BASIC': 9.99,
    'STANDARD': 49.99,
    'PREMIUM': 249.99
}

class CostExplorer:
    def __init__(self, plan: str, start_date: str, trial_days: int = 0):
        self.plan = plan
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.trial_days = trial_days
        self.plan_cost = PRICING[plan]

    def generate_report(self, current_date_str: str):
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        end_of_year = datetime(self.start_date.year, 12, 31)
        months = [calendar.month_name[m] for m in range(1, 13)]

        monthly_cost = {month: 0.0 for month in months}
        trial_end_date = self.start_date + timedelta(days=self.trial_days)
        billing_start_date = trial_end_date

        date = billing_start_date.replace(day=1)
        while date <= end_of_year:
            month_name = calendar.month_name[date.month]
            first_of_month = datetime(date.year, date.month, 1)
            last_of_month = datetime(date.year, date.month, \
            calendar.monthrange(date.year, date.month)[1])

            if billing_start_date > last_of_month:
                # Not billable, still in trial
                monthly_cost[month_name] = 0.0
            elif first_of_month < billing_start_date <= last_of_month:
                # Trial ends mid-month: prorate
                days_in_month = (last_of_month - first_of_month).days + 1
                billable_days = (last_of_month - billing_start_date).days + 1
                prorated = round(self.plan_cost * billable_days / days_in_month, 2)
                monthly_cost[month_name] = prorated
            elif first_of_month >= billing_start_date:
                monthly_cost[month_name] = self.plan_cost

            # Move to next month
            if date.month == 12:
                date = datetime(date.year + 1, 1, 1)
            else:
                date = datetime(date.year, date.month + 1, 1)

        # Trim months before billing starts
        report = {month: monthly_cost[month] for month in \
        months[billing_start_date.month - 1:]}
        total_yearly_cost = round(sum(report.values()), 2)

        return {
            'monthly_breakdown': report,
            'yearly_estimate': total_yearly_cost
        }
