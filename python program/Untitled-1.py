class Reservoir:
    def _init_(self, volume, nutrient_level):
        self.volume = volume
        self.nutrient_level = nutrient_level

class Pump:
    def _init_(self, flow_rate):
        self.flow_rate = flow_rate

    def circulate_nutrient(self, reservoir, trays):
        for tray in trays:
            reservoir.nutrient_level -= self.flow_rate
            tray.receive_nutrient(self.flow_rate)

class Tray:
    def _init_(self, capacity):
        self.capacity = capacity
        self.nutrient_level = 0

    def receive_nutrient(self, amount):
        self.nutrient_level += amount
        if self.nutrient_level > self.capacity:
            self.nutrient_level = self.capacity

if _name_ == "_main_":
    # Define parameters
    reservoir = Reservoir(volume=1000, nutrient_level=100)
    pump = Pump(flow_rate=10)
    trays = [Tray(capacity=500) for _ in range(4)]

    # Circulate nutrient
    pump.circulate_nutrient(reservoir, trays)

    # Display nutrient levels
    print("Reservoir Nutrient Level:", reservoir.nutrient_level)
    for i, tray in enumerate(trays, start=1):
        print(f"Tray {i} Nutrient Level:", tray.nutrient_level)