import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
from numpy.random import default_rng
from scipy.stats import skew, kurtosis

from .utils import generate_repeats
from .utils import incremental_filename
from .utils import check_path
from .report import skrisk_report
from .report import DEFAULT_PLOT_PALETTE, DEFAULT_PLOT_STYLE


class RiskProject(nx.DiGraph):
    """
    A class that represents and sets up a network used for visualizing and simulating risk management scenarios.

    Attributes:
        seed(int): Establishes the seed with which to perform all random operations.
        nsim(int): Number of simulations to perform when evaluating the entire network.
    """

    def __init__(self, seed=42, nsim=1000):
        super(RiskProject, self).__init__()
        self._seed = seed
        self.rng = default_rng(seed)
        self.nsim = nsim
        self.plot_palette = DEFAULT_PLOT_PALETTE
        self.plot_style = DEFAULT_PLOT_STYLE

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, new_seed):
        self._seed = new_seed
        self.rng = default_rng(new_seed)

    def binomial(self, n: int, p: float):  # TODO Add distributions as mixins
        """
        Returns a RiskProject.nsim-sized array of samples drawn from a binomial distribution.

        Parameters:
            n
                Number of trials for which success will be evaluated during each simulation.
            p
                Probability of success for each trial.
        """
        return self.rng.binomial(n, p, self.nsim)

    def triangular(self, left: float, mode: float, right: float):
        """
        Returns a RiskProject.nsim-sized array of randomly generated numbers using a triangular distribution.

        Parameters:
            left
                Lower limit of the distribution.
            mode
                Most likely value of the distribution.
            right
                Upper limit of the distribution.
        """
        return self.rng.triangular(left, mode, right, self.nsim)

    def gamma(self, shape, scale):
        """
        Returns a RiskProject.nsim-sized array of randomly generated numbers using a gamma distribution.

        Parameters:
            shape
                Lower limit of the distribution. # TODO: Change this description!
            scale
                Most likely value of the distribution.

        """
        return self.rng.gamma(shape, scale, self.nsim)

    def add_input(self, name: str, value: float, description=""):
        """
        Creates a node that will return a fixed value when evaluated.

        Parameters:
            name
                Name of the node.
            value
                Value returned when the node is evaluated.
            description
                Comprehensive summary about the node.
        """
        self.add_node(
            name, **{"value": value, "description": description, "node_type": "input"}
        )

    def add_random(
        self,
        name: str,
        distribution: str,
        parameters: tuple[str] | dict[str, object],
        description="",
        graphtype="histogram",
    ):
        """
        Creates a node that randomly generates observations inside a RiskProject.nsim-sized array according to the distribution specified when evaluated.

        Parameters:
            name
                Name of the node.
            distribution
                Name of the function whose result will be saved inside this node value attribute when this node is evaluated.
            parameters
                Parameters passed to the distribution.
            description
                Comprehensive summary about the node.
        """
        self.add_node(
            name,
            **{
                "value": None,
                "distribution": distribution,
                "parameters": parameters,
                "description": description,
                "node_type": "random",
                "stats": None,
                "graphtype": graphtype,
            },
        )

    def add_decision(
        self,
        name: str,
        incoming_nodes: tuple[str],
        condition,
        parameters,
        description="",
    ):
        # TODO: Decide whenever to scrap this method, or add related functionality in the eval method.
        """
        Creates a node that represents a decision point in the network.

        Parameters:
            name
                Name of the node.
            incoming_nodes
                Names of the nodes that the conditional will take as an input (in the form of a tuple).
            condition
                Condition to be fulfilled for the decision node to return True.
            description
                Comprehensive summary about the node.
        """
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

    def add_operation(
        self,
        name: str,
        operation: str,
        incoming_nodes: tuple[str, ...] | dict[str, str],
        description="",
        graphtype="histogram",
    ):
        """
        Creates a node that performs an operation on incoming nodes when evaluated.

        Parameters:
            name
                Name of the node.
            operation
                Name of the function (in the form of a string) whose result will be saved inside this node's value attribute when this node is evaluated.
            incoming_nodes
                Tuple with names for the input nodes whose value(s) will be taken as parameters for the function.
            description
                Comprehensive summary about the node.
        """
        self.add_node(
            name,
            **{
                "value": None,
                "operation": operation,
                "incoming_nodes": incoming_nodes,
                "description": description,
                "node_type": "operation",
                "stats": None,
                "graphtype": graphtype,
            },
        )
        if isinstance(incoming_nodes, dict):
            for param, node in incoming_nodes.items():
                self.add_edge(node, name, param=param)
        else:
            for node in incoming_nodes:
                self.add_edge(node, name)

    def add_goal(
        self,
        name: str,
        operation: str,
        incoming_nodes: tuple[str],
        description="",
        graphtype="histogram",
    ):
        """
        Creates a goal/output node, which serves as an endpoint for the network.

        Parameters:
            name
                Name of the node.
            operation
                Name of the function (in the form of a string) whose result will be saved inside this node's value attribute when this node is evaluated.
            incoming_nodes
                Tuple with names for the input nodes whose value(s) will be taken as parameters for the function.
            description
                Comprehensive summary about the node.
        """
        self.add_node(
            name,
            **{
                "value": None,
                "operation": operation,
                "incoming_nodes": incoming_nodes,
                "description": description,
                "node_type": "goal",
                "stats": None,
                "graphtype": graphtype,
            },
        )
        for node in incoming_nodes:
            self.add_edge(node, name)

    def validate_inputs(self):
        """

        Verifies if the input nodes in the network have other nodes pointing towards them, returning True if so.
        """
        return all([not self.in_degree(node) for node in self.input_nodes()])

    def validate_goals(self):
        # TODO: Make this function return True if all the nodes with "goal" as their node_type are connected to other nodes in the graph only as outputs.
        pass

    def input_nodes(self):
        """
        Returns a list of all the nodes whose node_type is "input".
        """
        return [node for node in self.nodes if self.nodes[node]["node_type"] == "input"]

    def random_nodes(self):
        """
        Returns a list of all the nodes whose node_type is "random".
        """
        return [
            node for node in self.nodes if self.nodes[node]["node_type"] == "random"
        ]

    def eval(self, node: str):
        """
        Fills out the "value" attribute of a node, doing the same for all other nodes pointing to it if necessary.
        This method uses the function name and parameters stored in the attributes of each node to generate the relevant RiskProject.nsim-sized arrays.

        Parameters
            node
                Name of the node to be evaluated (usually a goal node).
        """
        if node in self.input_nodes():
            return self.nodes[node]["value"]
        elif node in self.random_nodes():
            func = getattr(self, self.nodes[node]["distribution"])
            self.nodes[node]["value"] = func(**(self.nodes[node]["parameters"]))
            return self.nodes[node]["value"]
        else:
            param_map = {
                pred: self.get_edge_data(pred, node).get("param")
                for pred in self.predecessors(node)
                if self.get_edge_data(pred, node).get("param")
            }
            param = {pred: self.eval(pred) for pred in self.predecessors(node)}
            param = {param_map.get(key, key): param[key] for key in param}
            func = getattr(self, self.nodes[node]["operation"])
            self.nodes[node]["value"] = func(**param)
            return self.nodes[node]["value"]

    def generate_stats(self, node: str, ignore=None, additional=None):
        # TODO: Add the functionality related to the ignore/additional parameters.
        """
        Generates and adds to the node an attribute named "stats" from its eval-generated value attribute.

        Parameters
            node
                Name of the node whose statistics will be generated.
            ignore
                List of names of the stats that you don't want to generate.
                  additional
                List of tuples whose first value corresponds to the name of the statistics to be generated, and the second corresponds to the function used.
        """
        stats = {
            "mean": np.mean(self.nodes[node]["value"], axis=0),
            "max": np.max(self.nodes[node]["value"], axis=0),
            "min": np.min(self.nodes[node]["value"], axis=0),
            "std": np.std(self.nodes[node]["value"], axis=0),
            "median": np.median(self.nodes[node]["value"], axis=0),
            "skew": skew(self.nodes[node]["value"]),
            "kurt": kurtosis(self.nodes[node]["value"]),
        }
        self.nodes[node]["stats"] = stats
        return stats

    def print_stats(self, node: str):
        """
        Prints the stats attribute of a node inside a table.

        Parameters
            node
                Name of the node whose stats will be printed.
        """
        longesti = 0
        longestj = 0
        for i, j in self.nodes[node]["stats"].items():
            if len(i) > longesti:
                longesti = len(i)
            if len(str(j)) > longestj:
                longestj = len(str(j))
        fullwidth = longesti + longestj + 3
        print(("Stats for " + node).center(fullwidth))
        print("-" * fullwidth)
        if include != None:
            for i in include:
                print(
                    str(i).ljust(longesti)
                    + " # "
                    + str(self.nodes[node]["stats"][i]).rjust(longestj)
                )
        else:
            for i, j in self.nodes[node]["stats"].items():
                print(str(i).ljust(longesti) + " # " + str(j).rjust(longestj))
        return

    last_generated_graphic = (
        ""  # Variable where the location of the last generated graph is stored
    )

    def generate_histogram(
        self,
        node,
        title: str = "",
        file_path="/tmp/skrisk/",
        **kwargs,
    ):
        """
        Generates a histogram for a node.

        Parameters:
            node
                Node for which the histogram will be generated.
            title
                Title for the histogram.
            file_path
                Path where the histogram will be generated.
            **kwargs
                Miscellaneous arguments for the seaborn.histplot() function.
        """
        temp_file_path = check_path(file_path)
        hist_png_filename = incremental_filename(node, temp_file_path)
        sns.set_style(self.plot_style)
        sns.set_palette(self.plot_palette)
        sns.histplot(self.nodes[node]["value"], **kwargs).set(title=title)
        plt.savefig(hist_png_filename)
        self.last_generated_graphic = hist_png_filename
        print(f"Plot saved in file: {hist_png_filename}")
        plt.figure()

    def generate_piechart(
        self,
        node,
        title: str = "",
        file_path="/tmp/skrisk/",
        **kwargs,
    ):
        """
        Generates a pie chart for a node.
        """
        temp_file_path = check_path(file_path)
        hist_png_filename = incremental_filename(node, temp_file_path)

        sns.set_style(self.plot_style)
        sns.set_palette(self.plot_palette)
        palette = sns.color_palette(self.plot_palette)

        data, keys = generate_repeats(self.nodes[node]["value"])

        plt.title(title)
        plt.pie(data, labels=keys, colors=palette, autopct="%.0f%%", **kwargs)
        plt.savefig(hist_png_filename)
        self.last_generated_graphic = hist_png_filename
        print(f"Plot saved in file: {hist_png_filename}")

        plt.figure()

    def generate_report(self, file, skip=[], histogram_bins=10):
        """
        Generates a Markdown report for the current network. Automatically appends the contents of markdown files with the same name as any of the network's nodes if there are any.

        Parameters:
            file
                Name of the .md file to be generated.
            skip
                A tuple with the names of the nodes generate_report will skip.
            histogram_bins
                Number of bins in histograms.
        """

        return skrisk_report(self, file, skip, histogram_bins)

    def run(self):
        pass
