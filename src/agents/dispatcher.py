from src.data.loader import load_data
from src.optimization.solver import optimize_allocation

class Dispatcher:
    def __init__(self, data_source):
        self.data_source = data_source
        self.data = None
        self.allocations = None

    def load_data(self):
        self.data = load_data(self.data_source)

    def allocate_resources(self):
        if self.data is not None:
            self.allocations = optimize_allocation(self.data)
        else:
            raise ValueError("Data not loaded. Please load data before allocation.")

    def get_allocations(self):
        return self.allocations

    def run(self):
        self.load_data()
        self.allocate_resources()
        return self.get_allocations()