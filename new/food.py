from collections import defaultdict

class Driver:
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.deliveries = []
        self.paid_total  = 0
        self.unpaid_total = 0
        self.last_paid_index = 0


class Delivery:
    def __init__(self, ts, amount):
        self.ts = ts
        self.amount = amount


class Platform:
    def __init__(self):
        self.drivers = defaultdict()
    def add_driver(self, driver_id):
        if driver_id not in self.drivers:
            self.drivers[driver_id] = Driver(driver_id)
            print(f"{driver_id} added!")
        else:
            print(f"{driver_id} already present!")

    def add_delivery(self, driver_id, ts, amount):
        driver = self.drivers[driver_id]
        delivery = Delivery(ts, amount)
        driver.deliveries.append(delivery)
        driver.unpaid_total += amount
        print(f"Added delivery of {amount} at {ts} for driver: {driver_id}")

    def pay_up_to_time(self, driver_id, upto_ts):
        driver = self.drivers[driver_id]
        deliveries = driver.deliveries
        # for delivery in deliveries:
        #     if delivery.ts <= upto_ts:
        #         driver.unpaid_total -= delivery.amount
        #         driver.paid_total += delivery.amount

        while driver.last_paid_index < len(deliveries) and deliveries[driver.last_paid_index].ts <= upto_ts:
            driver.unpaid_total -= deliveries[driver.last_paid_index].amount
            driver.paid_total += deliveries[driver.last_paid_index].amount
            driver.last_paid_index += 1
        print(f"{driver.paid_total} paid upto {upto_ts}")

    def get_total_unpaid(self, driver_id):
        driver = self.drivers[driver_id]
        print(f"{driver.unpaid_total} unpaid for driver: {driver_id}")


plt = Platform()
plt.add_driver("driver1")
plt.add_delivery("driver1", 1, 100)
plt.add_delivery("driver1", 2, 200)
plt.add_delivery("driver1", 3, 300)
plt.get_total_unpaid("driver1")
plt.pay_up_to_time("driver1", 2)
plt.get_total_unpaid("driver1")
plt.pay_up_to_time("driver1", 3)
plt.get_total_unpaid("driver1")