class KvPair:
    def __init__(self):
        self.transactions = []
        self.realMap = {}

    def get(self, k): #O(txn stack length)
        for txn in reversed(self.transactions):
            if k in txn:
                return txn[k]
        return self.realMap[k] if k in self.realMap else "None"
    def set(self, k, v): #O(1)
        if  self.transactions:
            self.transactions[-1][k] = v
        else:
            self.realMap[k] = v
    def delete(self, k): #O(1)
        if  self.transactions:
            self.transactions[-1][k] = "NULL"
        else:
            self.realMap[k] = "NULL"
    def begin(self):
        self.transactions.append({})
    def commit(self):
        if not self.transactions:
            return "NO TRANSACTION"
        top = self.transactions.pop()
        if self.transactions:
            self.transactions[-1].update(top)
        else:
            self.realMap.update(top)
        return "COMMITTED"
    def rollback(self): #O(1)
        if len(self.transactions)!=0:
            return(self.transactions.pop())
        else:
            "NO TRANSACTION"
    # def commit(self):
    #     for k,v in self.transactions[-1].items():
    #         self.realMap[k] = v

    #     self.transactions = []
    #     return "committed"
    
    # Time: O(K)
    # (where K = number of keys in top transaction)
    
        

kv = KvPair()

print("Test 1: Set/Get/Delete without transactions")
kv.set("a", "foo")
# print(kv.)
print(kv.get("a") == "foo")
kv.delete("a")
print(kv.get("a") == "NULL")

print("Test 2: Simple transaction + rollback")
kv.set("x", "1")
kv.begin()
kv.set("x", "2")
kv.set("y", "2")
kv.begin()
print(kv.get("x") == "2")
kv.rollback()
print(kv.get("x") == "1")

print("Test 3: Nested transaction + commit")
kv.begin()
kv.set("x", "3")
kv.begin()
kv.set("x", "4")
print(kv.get("x"))
kv.commit()
print(kv.get("x"))

print("Test 4: Rollback after commit (should fail)")
result = kv.rollback()
print(result == "NO TRANSACTION")

print("Test 5: Delete inside transaction")
kv.set("z", "100")
kv.begin()
kv.delete("z")
print(kv.get("z") == "NULL")
kv.rollback()
print(kv.get("z") == "100")
kv.commit()
print(kv.get("z"))