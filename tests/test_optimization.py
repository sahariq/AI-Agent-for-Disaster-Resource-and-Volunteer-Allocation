import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'multi-agent-system'))
from workers.worker_optimization_agent import OptimizationWorkerAgent
import pandas as pd

class TestOptimization(unittest.TestCase):

    def setUp(self):
        self.agent = OptimizationWorkerAgent('test_opt_agent')
        self.severity_data = pd.DataFrame({
            'zone': ['zone_1', 'zone_2', 'zone_3'],
            'severity': [5, 3, 8]
        })
        self.available_volunteers = 50

    def test_allocate_resources(self):
        results, status, obj_value = self.agent.allocate_resources(self.severity_data, self.available_volunteers)
        self.assertIsInstance(results, dict)
        self.assertGreaterEqual(sum(results.values()), 0)

if __name__ == '__main__':
    unittest.main()
