class FoodDeliveryPlatform:
    def __init__(self):
        self.driverRateMap = {}
        self.deliveryMap = {}
        self.userPaidMap = {}
        self.userNotPaidMap = {}
    def addDriver(self, driver_id, hourly_rate):
        if driver_id not in self.driverRateMap:
            self.driverRateMap[driver_id] = hourly_rate
            self.deliveryMap[driver_id] = []
            self.userPaidMap = 0
            self.userNotPaidMap = 0
    def addDeliveries(self, driver_id, start_time, end_time):
        if driver_id not in self.deliveryMap:
            self.deliveryMap[driver_id]=[]

        self.deliveryMap[driver_id].append((start_time, end_time, False))
        time_elapsed = end_time - start_time

        cost_for_current_delivery = (time_elapsed/3600) * self.driverRateMap[driver_id]
        self.userNotPaidMap[driver_id] += cost_for_current_delivery
    def payUpToTIme(self, time, driver_id):

        if driver_id not in self.deliveryMap:
            print("Driver not present in our records!")
        all_deliveries = self.deliveryMap[driver_id]
        total_cost_under_time = 0
        for delivery in all_deliveries:
            if delivery[1] <= time and not delivery[2]:
                time_elapsed = delivery[1] - delivery[0]
                cost_for_current_delivery = (time_elapsed/3600) * self.driverRateMap[driver_id]
                total_cost_under_time += cost_for_current_delivery
        self.userPaidMap[driver_id] += total_cost_under_time
        return total_cost_under_time
    def getCostToBePaid(self, driver_id):
        if driver_id not in self.deliveryMap:
            print("Driver not present in our records!")
        
        return self.userNotPaidMap[driver_id] - self.userPaidMap[driver_id]


    
        

