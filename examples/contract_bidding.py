# %%
import sys
from pathlib import Path

# %%
BASE_DIR = Path.cwd().parent
sys.path.append(f"{BASE_DIR}")

# %%
import numpy as np
import pandas as pd

# %%
from skrisk import RiskProject

# %%


class ContractBiding(RiskProject):

    def num_competing_bids(self, num_competitors, prob_competitors):
        return self.binomial(num_competitors, prob_competitors)

    def competing_bids(
        self, param_competitors, num_competitors, project_cost, num_competing_bids
    ):
        return np.concatenate(
            (
                self.triangular(**param_competitors, size=num_competitors)
                * project_cost["mode"],
                np.full((4 - num_competing_bids[0],), np.inf),
            )
        )
    def win_contract(self, competing_bids, my_bid):
        return min(competing_bids) > my_bid

    def profit(self, win_contract, my_bid, project_cost, bid_cost):
        return (win_contract * (my_bid - project_cost)) - bid_cost


# %%

cb = ContractBiding()

cb.add_input("num_competitors", 4, "Number of Potential Competitors")
cb.add_input("prob_competitors", 0.5, "Probability a given competitor bids")
cb.add_rand_input(
    "bid_cost",
    "triangular",
    {"left": 300, "mode": 350, "right": 500},
    "Cost to prepare a bid",
)
cb.add_rand_input(
    "project_cost",
    "triangular",
    {"left": 9000, "mode": 10000, "right": 15000},
    "Cost to complete project",
)
cb.add_operation(
    "num_competing_bids",
    ("num_competitors", "prob_competitors"),
    # num_competing_bids,
    "Number of competing bids",
)
cb.add_operation(
    "competing_bids",
    ("num_competing_bids"),
    # competing_bids,
    "Competing Bids",
)
cb.add_input(
    "my_bid",
    10500,
    "Miller's bid"
)
cb.add_rand_input(
    "project_cost",
    "triangular",
    {"left": 9000, "mode": 10000, "right": 15000}
)
cb.add_rand_input(
    "bid_cost",
    "triangular",
    {"left": 300, "mode": 350, "right": 500}
)
cb.add_operation(
    "win_contract",
    ("competing_bids", "my_bid")
)

cb.add_goal(
    "profit",
    ("win_contract", "project_cost")
)
