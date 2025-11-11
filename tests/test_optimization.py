import unittest
from src.optimization.solver import allocate_resources
from src.optimization.model import create_model
from src.optimization.constraints import add_constraints

class TestOptimization(unittest.TestCase):

    def setUp(self):
        self.model = create_model()
        self.resources = {
            'ambulances': 10,
            'doctors': 20,
            'nurses': 30
        }
        self.severity = {
            'zone_1': 5,
            'zone_2': 3,
            'zone_3': 8
        }

    def test_allocate_resources(self):
        allocation = allocate_resources(self.model, self.resources, self.severity)
        self.assertIsInstance(allocation, dict)
        self.assertGreaterEqual(sum(allocation.values()), 0)

    def test_model_creation(self):
        self.assertIsNotNone(self.model)

    def test_add_constraints(self):
        constraints = add_constraints(self.model, self.resources)
        self.assertTrue(constraints)

if __name__ == '__main__':
    unittest.main()