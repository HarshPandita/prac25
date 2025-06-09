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
