import networkx as nx
from numpy.random import default_rng


class RiskProject(nx.DiGraph):
    """_summary_

    Args:
        nx (_type_): _description_
    """

    def __init__(self, seed=42, nsim=1000):
        self._seed = seed
        self.rng = default_rng(seed)
        self.nsim = nsim

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, new_seed):
        self._seed = new_seed
        self.rng = default_rng(new_seed)

    def binomial(self, n, p):
        return self.rng.binomial(n, p, self.nsim)

    def triangular(self, left, mode, right):
        return self.rng.triangular(left, mode, right, self.nsim)

    def add_input(self, name, value, description=""):
        self.add_node(
            name, {"value": value, "description": description, "node_type": "input"}
        )

    def add_rand_input(self, name, distribution, parameters, description=""):
        self.add_node(
            name,
            {
                "distribution": distribution,
                "parameters": parameters,
                "description": description,
                "node_type": "rand_input",
            },
        )

    def add_decision(self, name, incoming_nodes, condition, parameters, description=""):
        self.add_node(
            name,
            {
                "incoming_nodes": incoming_nodes,
                "condition": condition,
                "description": description,
                "node_type": "decision",
            },
        )
        for node in incoming_nodes:
            self.add_edge(node, name)

    def add_operation(self, name, incoming_nodes, operation, description):
        self.add_node(
            name,
            {
                "operation": operation,
                "incoming_nodes": incoming_nodes,
                "description": description,
                "node_type": "operation",
            },
        )
        for node in incoming_nodes:
            self.add_edge(node, name)

    def add_goal(self, name, incoming_nodes, operation, description):
        self.add_node(
            name,
            {
                "incoming_nodes": incoming_nodes,
                "operation": operation,
                "description": description,
                "node_type": "goal",
            },
        )
        for node in incoming_nodes:
            self.add_edge(node, name)

    def run(self):
        pass
