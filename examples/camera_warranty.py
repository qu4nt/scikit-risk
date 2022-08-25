# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


# %%
BASE_DIR = Path.cwd()
sys.path.append(f"{BASE_DIR}")


# %%
import numpy as np
import pandas as pd


# %%
from skrisk import RiskProject


# %%
class WarrantyCost(RiskProject):

    def lifetime_of_camera(self, shape, scale):
        return pd.DataFrame(self.gamma(shape, scale))

    def time_of_failure(self, camera_lifetime):
        pass

    def cost_to_company(self, warranty_period, camera_lifetime, replacement_cost):
        pass

    def discounted_cost(self, time_of_failure, cost_to_company, discount_rate):
        pass

    def failures_within_warranty(self, warranty_period):
        pass

    def npv_of_profit(self, discounted_cost, replacement_cost, cost_for_customer):
        pass

