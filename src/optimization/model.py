class OptimizationModel:
    def __init__(self, severity_data, volunteer_data):
        self.severity_data = severity_data
        self.volunteer_data = volunteer_data
        self.model = None

    def define_objective(self):
        self.model += lpSum(self.severity_data[i] for i in range(len(self.severity_data)))

    def create_model(self):
        from pulp import LpProblem, LpMinimize

        self.model = LpProblem("Disaster_Resource_Allocation", LpMinimize)
        self.define_objective()

    def solve(self):
        self.model.solve()
        return {v.name: v.varValue for v in self.model.variables()}

    def get_results(self):
        return {
            "status": self.model.status,
            "objective_value": self.model.objective.value(),
            "variables": {v.name: v.varValue for v in self.model.variables()}
        }