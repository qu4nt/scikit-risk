# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

# %%
BASE_DIR = Path.cwd()
sys.path.append(f"{BASE_DIR}")

# %%
import numpy as np
import pandas as pd

# %%
from skrisk import RiskProject

# %%


class ContractBiding(RiskProject):
    def num_competing_bids(self, num_competitors, prob_competitors):
        return pd.DataFrame(self.binomial(num_competitors, prob_competitors))

    def competing_bids(self, param_competitors, num_competing_bids):
        return num_competing_bids.apply(
            lambda x: self.rng.triangular(**param_competitors, size=x)
            * self.nodes["project_cost"]["parameters"]["mode"],
            axis=1,
        )

    def win_contract(self, competing_bids, my_bid):
        competitors_best_bid = competing_bids.apply(
            lambda x: x.min() if x.size else np.inf
        )
        return competitors_best_bid > my_bid

    def profit(self, win_contract, my_bid, project_cost, bid_cost):
        return (win_contract * (my_bid - project_cost)) - bid_cost


# %%

cb = ContractBiding()

cb.add_input("num_competitors", 4, "Number of Potential Competitors")
cb.add_input("prob_competitors", 0.5, "Probability a given competitor bids")
cb.add_input(
    "param_competitors",
    {"left": 0.9, "mode": 1.3, "right": 1.8},
    "Base competitors parameters",
)
cb.add_random(
    "bid_cost",
    "triangular",
    {"left": 300, "mode": 350, "right": 500},
    "Cost to prepare a bid",
)
cb.add_random(
    "project_cost",
    "triangular",
    {"left": 9000, "mode": 10000, "right": 15000},
    "Cost to complete project",
)
cb.add_operation(
    "num_competing_bids",
    "num_competing_bids",
    ("num_competitors", "prob_competitors"),
    "Number of competing bids",
)
cb.add_operation(
    "competing_bids",
    "competing_bids",
    ("param_competitors", "num_competing_bids"),
    "Competing Bids",
)
cb.add_input("my_bid", 10500, "Miller's bid")
cb.add_random(
    "project_cost", "triangular", {"left": 9000, "mode": 10000, "right": 15000}
)
cb.add_random("bid_cost", "triangular", {"left": 300, "mode": 350, "right": 500})
cb.add_operation(
    "win_contract",
    "win_contract",
    ("competing_bids", "my_bid"),
    "Miller wins contract?",
)

cb.add_goal(
    "profit", "profit", ("win_contract", "my_bid", "project_cost", "bid_cost"), "profit"
)
# %%
profit = cb.eval("profit")
print(profit)
sns.histplot(profit, bins=30).set(title=f'Millers Bid: {cb.nodes["my_bid"]["value"]}')
plt.savefig('millers_bid.png')
plt.figure()

# %%
pos = nx.nx_pydot.pydot_layout(cb, prog="dot")
nx.draw(cb, pos=pos, with_labels=True, font_weight="bold")
plt.savefig('millers_problem.png')
plt.show()