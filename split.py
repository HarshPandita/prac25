from collections import defaultdict, deque

class Splitwise:
    def __init__(self, transactions):
        self.transactions = transactions
        self.balance = defaultdict(int)
        self.debt_queue = deque()
        self.credit_queue = deque()

    def _calculate_balances(self):
        for frm, to, amt in self.transactions:
            self.balance[frm] -= amt
            self.balance[to] += amt

    def _create_queues(self):
        for person, val in self.balance.items():
            if val < 0:
                self.debt_queue.append((person, -val))
            elif val > 0:
                self.credit_queue.append((person, val))

    def _settle_balances(self):
        result = []
        while self.debt_queue and self.credit_queue:
            debtor, debt_amt = self.debt_queue.popleft()
            creditor, cred_amt = self.credit_queue.popleft()

            settled_amt = min(debt_amt, cred_amt)
            result.append((debtor, creditor, settled_amt))

            if debt_amt > cred_amt:
                self.debt_queue.append((debtor, debt_amt - cred_amt))
            elif cred_amt > debt_amt:
                self.credit_queue.append((creditor, cred_amt - debt_amt))
        return result

    def split(self):
        self._calculate_balances()
        self._create_queues()
        return self._settle_balances()
