import numpy as np


def get_hhmmss(seconds):
    ss = seconds % 60
    minutes = seconds // 60
    mm = minutes % 60
    hh = minutes // 60
    return hh, mm, ss


def save_data(filename, data):
    dim = np.ndim(data)
    with open(filename, "w") as f:
        if dim == 0:
            f.write(str(data))
        elif dim == 1:
            f.write(" ".join([str(val) for val in data]))
        elif dim == 2:
            for row in data:
                f.write(" ".join([str(val) for val in row]) + "\n")
        else:
            raise ValueError(
                "data dimension is invalid. Try saving data with dimension 0~2"
            )


def load_series(content):
    c = []
    for i in np.arange(len(content)):
        ci = np.array(list(content[i]))
        c.append(ci)
    c = np.array(c)
    return c


def get_return_probability(N, inc):
    """
    Output:
    Generate N anual return probability with increment inc.

    Input:
    (N) int - the number of return probability
    (inc) int - increment between return period
    """
    probability = np.zeros(N)
    probability[0] = 1 - 1 / inc
    probability[1:] = (1.0 / np.arange(1, N) - 1.0 / np.arange(2, N + 1)) / inc
    probability = np.asarray(probability).astype("float64")
    probability[-1] = 1.0 - np.sum(probability[0:-2])
    probability /= probability.sum()  # generate distribution for surge
    return probability


def cond_normal_generator(data, dataO, X):
    """
    Output:
    Generate the conditional normal distribution parameters mu(Xk|Xk-1) and sigma(Xk|Xk-1)
    Input:
    (data) N*M numpy matrix - M dependent normal distributions each with N samples.
    (dataO) N*M numpy matrix - the original distribution of X
    (X) single - observed data for k-1

    NOTE: Data must not be non-repetitive from distribution to distribution!!!
    """
    # Get the unconditioned normal parameters and cross-correlation

    muY = np.mean(data, axis=0)
    sigY = np.std(data, axis=0)
    muX = np.mean(dataO)
    sigX = np.std(dataO)
    muYX = []
    sigYX = []
    for i in np.arange(data.shape[1]):
        muYi = muY[i]
        sigYi = sigY[i]
        rho = np.corrcoef(dataO, data[:, i])[0, 1] * (1 - i * 0.02)
        muYXi = muYi + rho * (sigYi / sigX) * (X - muX)
        sigYXi = (sigYi**2 * (1 - rho**2)) ** 0.5
        muYX.append(muYXi[0])
        sigYX.append(sigYXi)
    return muYX, sigYX


def make_non_decreasing(arr):
    # Calculate the cumulative maximum along the array

    cummax = np.maximum.accumulate(arr)
    # Replace elements in the original array with the cumulative maximum

    arr_non_decreasing = np.maximum(arr, cummax)
    return arr_non_decreasing