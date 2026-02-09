# code for txn enabled kv pair

from app.api.lead import get_lead_audit_trail


class kvPair:
    def __init__(self):
        self.cache = {}
        self.txns = []

    def get_latest_txn(self):
        if len(self.txns)>0:
            return  self.txns[-1]
        return None
    # GET KEY
    # IF TXN - GET KEY FROM THAT LAYER
    # IF NOT - GET FROM SELF CACHE
    def get(self,key):
        for txn in reversed(self.txns):
            if key in txn["data"][key]:
                print("found in txn")
                print(txn["data"]["key"])
                return txn["data"][key]

        if key in self.cache:
            print(self.cache[key])
            return self.cache[key]
        else:
            print("key not found")


    def set(self, key, val):
        latest_txn = self.get_latest_txn()
        if latest_txn:
            latest_txn["data"][key] = val

        else:
            self.cache[key] = val
        return val

    def evict(self, key):
        latest_txn = self.get_latest_txn()
        if latest_txn:
            value = latest_txn["data"][key]
            del latest_txn["data"][key]
            latest_txn["deleted"].append(value)

        else:
            del self.cache[key]

    def commit(self):
        if not self.txns:
            return "No txn to commit!"
        current_txn = self.txns.pop()
        parent_txn = self.get_latest_txn()
        if parent_txn:
            parent_txn["data"].update(current_txn["data"])
            parent_txn["deleted"].update[current_txn["deleted"]]
        else:
            for key in current_txn["deleted"]:
                self.cache.pop(key)
            self.cache.update(current_txn["data"])

    def begin(self):
        self.txns.append({"data":{},"deleted":set()})
    def rollback(self):
        if self.get_latest_txn():
            self.txns.pop()
        else:
            print("no txn to rollback")



obj = kvPair()
obj.set("1","1")
obj.begin()
obj.set("1","2")
obj.get("1")
obj.commit()
# obj.get("1")
# obj.rollback()
# obj.get("1")







