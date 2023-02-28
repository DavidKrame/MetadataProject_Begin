import os
import shutil
import argparse
from datetime import datetime, timedelta
import pandas as pd
import math
import numpy as np
import random
from copy import deepcopy
from tqdm import trange

from pandas import read_csv, DataFrame
from scipy import stats

parser = argparse.ArgumentParser()
parser.add_argument('--dataset-name', default='TS1.csv',
                    help='Name of the dataset')
parser.add_argument('--window-length', default=6,
                    help='Name of the dataset')
parser.add_argument('--lag', default=5,
                    help='Desired delay')
parser.add_argument('--horizon', default=1,
                    help='Desired prediction time horizon')


def create_npy(path, location_dir="datas_npy"):
    data_frame = pd.read_csv(path, sep=";", index_col=0,
                             parse_dates=True, decimal=",")

    data_frame.fillna(0, inplace=True)

    columns = list(data_frame.columns)
    print("COLUMN'S NAMES IN INPUT DATA")
    print(columns)
    print("\t\n")

    try:
        os.mkdir(location_dir)
    except FileExistsError:
        pass

    for column in columns:
        data_npy = np.array(data_frame[column].values)
        location = os.path.join(location_dir, f"{column}")
        np.save(location, data_npy)


def chunking_function(array, window_length: int):
    chunks = []
    if window_length >= 6:
        pass
    else:
        window_length = 6

    for i in range((len(array)-window_length) + 1):
        chunk = array[i: i+window_length]
        chunks.append(chunk)
    chunks = np.array(chunks)

    return chunks


def create_chunked_npy(path_in, path_out="datas_chunked_npy", window_length=4):

    path_of_npy = path_in

    try:
        os.mkdir(path_out)
    except FileExistsError:
        pass

    for filename in os.listdir(path_of_npy):
        f = os.path.join(path_of_npy, filename)
        if os.path.isfile(f) and f.endswith("npy"):
            data = np.load(f)

            f_name = f.split("\\")[-1]
            chunks = chunking_function(data, window_length)
            final_location = os.path.join(path_out, f_name)

            np.save(final_location, chunks)


def compute_quartile(order: int, one_dim_array):
    one_dim_array.sort()
    N = len(one_dim_array)

    if order == 1:
        numerator_quartile = N+3
    elif order == 2:
        numerator_quartile = 2*N+2
    elif order == 3:
        numerator_quartile = 3*N+1

    else:
        raise ValueError("Order must be between 1,2 and 3")

    indice_quartile = (numerator_quartile//4)-1

    if (numerator_quartile % 4 == 0):
        quartile = one_dim_array[indice_quartile]
    elif (numerator_quartile % 4 == 1):
        quartile = (
            one_dim_array[indice_quartile]*3 + one_dim_array[indice_quartile+1])/4
    elif (numerator_quartile % 4 == 2):
        quartile = (
            one_dim_array[indice_quartile] + one_dim_array[indice_quartile+1])/2
    elif (numerator_quartile % 4 == 3):
        quartile = (
            one_dim_array[indice_quartile] + one_dim_array[indice_quartile+1]*3)/4

    return quartile


def compute_all_quartiles(one_dim_ar):
    one_dim_array = deepcopy(one_dim_ar)
    one_dim_array.sort()

    minimum = one_dim_array[0]
    maximum = one_dim_array[-1]

    first_quartile = compute_quartile(1, one_dim_array)
    second_quartile = compute_quartile(2, one_dim_array)
    third_quartile = compute_quartile(3, one_dim_array)

    quartiles = [minimum, first_quartile,
                 second_quartile, third_quartile, maximum]

    return quartiles


def saving_quartiled_datas(lag: int, horizon: int, path_in, path_out="datas_quartiles_npy"):
    assert (
        horizon >= 1), f"Horizon must be rather than 0. You provide {horizon}"
    assert (lag >= 5), f"Lag must be rather than 5. You provide {lag}"
    try:
        os.mkdir(path_out)
    except FileExistsError:
        pass

    for filename in os.listdir(path_in):
        f = os.path.join(path_in, filename)
        if (os.path.isfile(f) and f.endswith("npy")):
            data_in = np.load(f)
            window_len = data_in.shape[1]

            assert (lag + horizon ==
                    window_len), f"LAG + HORIZON must be equal to WINDOW."

            data_out = []
            for elt in data_in:
                out1 = compute_all_quartiles(elt[:-(horizon)])
                out2 = elt[lag:]
                out = out1
                for x in out2:
                    out.append(x)
                data_out.append(out)
            f_name = f.split("\\")[-1]
            data_out = np.array(data_out)

            final_location = os.path.join(path_out, f_name)

            np.save(final_location, data_out)


# def global_function(path_datas, paths_npy, path_chunked_npy, path_out_chunked_npy, path_out_quartiled_npy=, window_len: int, lag: int, horizon: int)


if __name__ == "__main__":
    args = parser.parse_args()

    path = args.dataset_name
    window = args.window_length
    horizon = args.horizon
    lag = args.lag

    input_dir = "datas_npy"
    output_dir = "datas_chunked_npy"
    path_out_quartiled_npy = "datas_quartiles_npy"

    try:
        shutil.rmtree(input_dir)
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(output_dir)
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(path_out_quartiled_npy)
    except FileNotFoundError:
        pass

    create_npy(path)
    create_chunked_npy(input_dir, output_dir, window_length=int(window))

    saving_quartiled_datas(lag=int(lag), horizon=int(horizon), path_in=output_dir,
                           path_out=path_out_quartiled_npy)

    # Demonstration
    dt = np.load("datas_chunked_npy\\VAL_1.npy")
    print("\t 2 HEAD VALUES IN DATAS_CHUNKED")
    print(dt[:2])
    print("\n")
    print("\t 2 HEAD VALUES IN DATAS_QUARTILED")
    dt2 = np.load("datas_quartiles_npy\\VAL_1.npy")
    print(dt2[:2])
