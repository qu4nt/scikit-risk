import os
import collections


def generate_repeats(arr: list):
    """Generates the amount of repetitions and names of values in an array in two arrays with matching indexes."""
    c = collections.Counter(arr)
    data_values = [c[i] for i in c]
    data_keys = [str(i) for i in c]
    return data_values, data_keys


def incremental_filename(node, temporal_path: str) -> str:
    i = 1
    hist_png_filename = f"{temporal_path}{node}_histogram_{i}.png"
    while os.path.exists(hist_png_filename):
        i += 1
        hist_png_filename = f"{temporal_path}{node}_histogram_{i}.png"
    return hist_png_filename


def check_path(path: str) -> str:
    path = path
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def node_title(node_name: str) -> str:
    return node_name.replace("_", " ").title()
