import networkx as nx
from numpy.random import default_rng


class RiskProject(nx.DiGraph):
    """_summary_

    Args:
        nx (_type_): _description_
    """

    def __init__(self, seed=42, nsim=1000):
        super(RiskProject, self).__init__()
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

    def binomial(self, n, p):  # TODO Add distributions as mixins
        return self.rng.binomial(n, p, self.nsim)

    def triangular(self, left, mode, right):
        return self.rng.triangular(left, mode, right, self.nsim)

    def add_input(self, name, value, description=""):
        self.add_node(
            name, **{"value": value, "description": description, "node_type": "input"}
        )

    def add_random(self, name, distribution, parameters, description=""):
        self.add_node(
            name,
            **{
                "value": None,
                "distribution": distribution,
                "parameters": parameters,
                "description": description,
                "node_type": "random",
            },
        )

    def add_decision(self, name, incoming_nodes, condition, parameters, description=""):
        self.add_node(
            name,
            **{
                "value": None,
                "condition": condition,
                "incoming_nodes": incoming_nodes,
                "description": description,
                "node_type": "decision",
            },
        )
        for node in incoming_nodes:
            self.add_edge(node, name)

    def add_operation(self, name, operation, incoming_nodes, description=""):
        self.add_node(
            name,
            **{
                "value": None,
                "operation": operation,
                "incoming_nodes": incoming_nodes,
                "description": description,
                "node_type": "operation",
            },
        )
        for node in incoming_nodes:
            self.add_edge(node, name)

    def add_goal(self, name, operation, incoming_nodes, description=""):
        self.add_node(
            name,
            **{
                "value": None,
                "operation": operation,
                "incoming_nodes": incoming_nodes,
                "description": description,
                "node_type": "goal",
            },
        )
        for node in incoming_nodes:
            self.add_edge(node, name)

    def validate_inputs(self):
        return all([not self.in_degree(node) for node in self.input_nodes()])

    def validate_goals(self):
        pass

    def input_nodes(self):
        return [node for node in self.nodes if self.nodes[node]["node_type"] == "input"]

    def random_nodes(self):
        return [node for node in self.nodes if self.nodes[node]["node_type"] == "random"]

    def eval(self, node):
        if node in self.input_nodes():
            return self.nodes[node]["value"]
        elif node in self.random_nodes():
            func = getattr(self, self.nodes[node]["distribution"])
            self.nodes[node]["value"] = func(**(self.nodes[node]["parameters"]))
            return self.nodes[node]["value"]
        else:
            param = {pred: self.eval(pred) for pred in self.predecessors(node)}
            func = getattr(self, self.nodes[node]["operation"])
            self.nodes[node]["value"] = func(**param)
            return self.nodes[node]["value"]

    def run(self):
        pass
