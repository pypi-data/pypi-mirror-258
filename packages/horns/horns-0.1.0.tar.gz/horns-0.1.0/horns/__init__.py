from multiprocessing import Pool
from typing import Literal, Optional

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.figure import Figure
from numba import njit, prange
from numba.core import config
from scipy import optimize
from scipy.stats import multivariate_normal, rankdata
from numba_stats import norm
from tqdm import tqdm

config.THREADING_LAYER = "threadsafe"

RanMeths = Literal["shuffle", "bootstrap", "normal", "uniform"]


@njit(parallel=True, fastmath=True)
def _rand(data: np.ndarray, method: RanMeths) -> np.ndarray:
    """Generate random data.

    Available methods are "normal", "uniform", "shuffle", and "bootstrap". "normal" will
    generate random data from a standard normal distribution. "uniform" will generate
    random data from a standard uniform distribution. "shuffle" will shuffle the data in
    each column, maintaining the original distribution of each variable but removing its
    correlation structure. "bootstrap" will generate new columns by sampling with
    replacement from each column.

    Args:
        data: Original data.
        method: Method to use.

    Returns:
        Random data.

    """
    n, m = data.shape
    out = np.empty((n, m), dtype=data.dtype)

    if method == "normal":
        for i in prange(n):
            for j in prange(m):
                # surprisingly, this is faster than np.random.normal(size=(n, m))
                out[i, j] = np.random.normal()

    elif method == "uniform":
        for i in prange(n):
            for j in prange(m):
                out[i, j] = np.random.uniform()

    elif method == "shuffle":
        for i in prange(m):
            out[:, i] = np.random.permutation(data[:, i])
    else:
        for i in prange(m):
            out[:, i] = np.random.choice(data[:, i], size=n, replace=True)

    return out


@njit(parallel=True, fastmath=True)
def _rands(data: np.ndarray, s: int, method: RanMeths) -> np.ndarray:
    """Generate `s` random datasets.

    Random datasets have the same shape as the original dataset but no underlying
    correlation structure.

    Args:
        data: Original data.
        s: Number of datasets to generate.
        method: Method to use.

    Returns:
        Random datasets.

    """
    n, m = data.shape
    out = np.empty((s, n, m), dtype=data.dtype)

    for i in prange(s):
        out[i] = _rand(data, method)

    return out


AnTypes = Literal["pca", "fa"]


@njit(parallel=True, fastmath=True)
def _eig(a: np.ndarray, analysis_type: AnTypes) -> np.ndarray:
    """Compute eigenvalues of a matrix.

    Assumes that the matrix is real-valued and symmetric.

    Args:
        a: Matrix.
        analysis_type: Type of analysis being performed. Either "pca" or "fa".

    Returns:
        Eigenvalues.

    """
    if analysis_type == "pca":
        return np.linalg.eigvals(a)

    else:
        aplus = np.linalg.pinv(a)
        d = np.diag(np.diag(aplus))
        p = np.linalg.pinv(d)
        return np.linalg.eigvals(a - p)


@njit(parallel=True, fastmath=True)
def _eigs(a: np.ndarray, analysis_type: AnTypes) -> np.ndarray:
    """Compute eigenvalues of all datasets.

    Args:
        a: Three-dimensional array of datasets.
        analysis_type: Type of analysis.

    Returns:
        Eigenvalues.

    """
    s, n, m = a.shape
    out = np.empty((s, m), dtype=np.float64)

    for i in prange(s):
        out[i] = _eig(a[i], analysis_type)

    return out


@njit(fastmath=True)
def _pearson(data: np.ndarray) -> np.ndarray:
    """Calculate the Pearson correlation matrix.

    Args:
        data: Data.

    Returns:
        Correlation matrix.

    """
    return np.corrcoef(data, rowvar=False)


@njit(parallel=True, fastmath=True)
def _pearsons(a: np.ndarray) -> np.ndarray:
    """Calculate the Pearson correlation matrices for all datasets.

    Args:
        a: Three-dimensional array of datasets.

    Returns:
        Correlation matrix.

    """
    s, n, m = a.shape
    out = np.empty((s, m, m), dtype=np.float64)

    for i in prange(s):
        out[i] = _pearson(a[i])

    return out


def _spearman(data: np.ndarray) -> np.ndarray:
    """Calculate the Spearman correlation matrix.

    Args:
        data: Data.

    Returns:
        Correlation matrix.

    """
    return _pearson(rankdata(data, axis=0))


def _spearmans(a: np.ndarray) -> np.ndarray:
    """Calculate the Spearman correlation matrices for all datasets.

    Args:
        a: Three-dimensional array of datasets.

    Returns:
        Correlation matrix.

    """
    with Pool() as pool:
        mats = np.array(pool.map(_spearman, a))

    return mats


Cont = tuple[np.ndarray, np.ndarray, np.ndarray]


@njit(parallel=True, fastmath=True)
def _contingency(x: np.ndarray, y: np.ndarray) -> Cont:
    """Create a contingency table assuming x and y are both ordinal.

    Args:
        x: First vector of data.
        y: Second vector of data.

    Returns:
        Unique values of x, unique values of y, and the contingency table.

    """
    ux = np.unique(x)
    uy = np.unique(y)
    shape = (ux.size, uy.size)
    t = np.zeros(shape, dtype=float)
    for i in prange(ux.size):
        for j in prange(uy.size):
            t[i, j] = np.sum((x == ux[i]) & (y == uy[j]))
    return ux, uy, t


@njit(parallel=False, fastmath=True)
def _thresholds(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Calculate the thresholds for the polychoric correlation coefficient.

    Args:
        t: Contingency table.

    Returns:
        Thresholds.

    """
    l_ = np.array([-23])
    u = np.array([23])
    cx = np.cumsum(np.sum(t, axis=0))
    cx = cx / cx[-1]
    px = np.concatenate((l_, norm.ppf(cx[:-1], 0.0, 1.0), u))  # noqa
    cy = np.cumsum(np.sum(t, axis=1))
    cy = cy / cy[-1]
    py = np.concatenate((l_, norm.ppf(cy[:-1], 0.0, 1.0), u))  # noqa
    return px, py


def _nll(rho: float, t: np.ndarray, px: np.ndarray, py: np.ndarray) -> float:
    """Calculate the negative log-likelihood of the polychoric model.

    Args:
        rho: Polychoric correlation coefficient.
        t: Contingency table.
        px: Thresholds for x.
        py: Thresholds for y.

    Returns:
        Negative log-likelihood.

    """
    out = np.zeros_like(t, dtype=float)
    dist = multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]])

    for i in prange(1, px.size):
        for j in prange(1, py.size):
            ll = dist.logcdf((px[i], py[j]), lower_limit=(px[i - 1], py[j - 1]))
            out[i - 1, j - 1] = ll

    return -1 * np.sum(t * out)


def _poly(x: np.ndarray, y: np.ndarray) -> float:
    """Compute the polychoric correlation coefficient.

    Args:
        x: First vector of data.
        y: Second vector of data.

    Returns:
        Polychoric correlation coefficient.

    """
    _, _, t = _contingency(x, y)
    px, py = _thresholds(t)
    return optimize.fminbound(_nll, -0.999, 0.999, args=(t, px, py))  # noqa


def _polychoric(data: np.ndarray) -> np.ndarray:
    """Calculate the polychoric correlation matrix.

    Args:
        data: Data.

    Returns:
        Correlation matrix.

    """
    n, m = data.shape
    args = []

    for i in range(m):
        for j in range(i + 1, m):
            x = data[:, i]
            y = data[:, j]
            args.append((x, y))

    try:
        with Pool() as pool:
            results = pool.starmap(_poly, args)

    except AssertionError:
        results = [_poly(*arg) for arg in args]

    out = np.eye(m)
    for i in range(m):
        for j in range(i + 1, m):
            out[i, j] = out[j, i] = results.pop(0)

    return out


def _polychorics(a: np.ndarray) -> np.ndarray:
    """Calculate the polychoric correlation matrices for all datasets.

    Args:
        a: Three-dimensional array of datasets.

    Returns:
        Correlation matrix.

    """
    results = []

    try:
        with Pool() as pool:
            results = pool.map(_polychoric, a)

    except AssertionError:
        for _a in tqdm(a):
            results.append(_polychoric(_a))

    return np.array(results)


arr = np.array
PaTypes = int | tuple[int, Figure]
FunTypes = Optional[callable | Literal["pearson", "spearman", "polychoric"]]


def parallel_analysis(
    data: np.ndarray,
    simulations: int = int(1e4),
    randomisation_method: RanMeths = "normal",
    analysis_type: AnTypes = "pca",
    quartile: float = 0.95,
    matrix_function: FunTypes = None,
    return_figure: bool = False,
) -> PaTypes:
    """Perform parallel analysis.

    Parallel analysis involves simulating a large number of random datasets with the
    same shape as the original dataset but with no underlying correlation structure. We
    calculate the eigenvalues of the random datasets and the `q`th quantile of the
    distribution of each eigenvalue, as well as the eigenvalues of the original dataset.
    The original eigenvalues are then compared to the quantiles. The number of
    components/factors to retain is the number of original eigenvalues that are greater
    than their corresponding quantile until we encounter the first eigenvalue that is
    not greater than its quantile.

    Args:
        data: An array-like object with shape (n, m), where n is the number of
            observations per variable and m is the number of variables.
        simulations: A positive integer representing the number of simulations to run.
            The default is 100,000. You may wish to reduce this number if you are
            working with a large dataset or on a slow machine.
        randomisation_method: How to generate a random dataset per simulation. Must be
            one of "shuffle", "bootstrap", "normal", or "uniform". "shuffle" will
            shuffle the data in each column, maintaining the original distribution of
            each variable but removing its correlation structure. "bootstrap" will
            generate new columns by sampling with replacement from each column (this is
            probably a better choice than "shuffle"). "normal" will generate random data
            from a standard normal distribution (the default). "uniform" will generate
            random data from a standard uniform distribution.
        analysis_type: Type of analysis to perform. Must be one of "pca" or "fa". "pca"
            (the default) will perform principal component analysis. "fa" will perform
            factor analysis. This is important because the eigenvalues will be
            calculated differently depending on the type of analysis.
        quartile: Quantile to use. Must be a float between 0 and 1. The default is 0.95.
        matrix_function: Optional custom function to calculate the covariance or
            correlation matrix of each random dataset and the original dataset. Must
            accept a two-dimensional array and return a two-dimensional array. If not
            provided, the Pearson correlation matrix will be used. Note that this
            function should be efficient, as it will be called many times.
        return_figure: Whether to return a figure. The default is False.

    Returns:
        If `return_figure` is False and `return_eigenvalues` is False, the number of
        components/factors to retain. If `return_figure` is True, a tuple containing the
        number of components/factors to retain and the figure. If `return_eigenvalues`
        is True, a tuple containing the number of components/factors to retain and the
        eigenvalues of the original dataset and the simulated datasets. If both
        `return_figure` and `return_eigenvalues` are True, a tuple containing the number
        of components/factors to retain, the figure, and the eigenvalues of the original
        dataset and the simulated datasets.

    """
    if matrix_function in (None, "pearson", "pearsonr", "r"):
        mf = _pearson
        mfs = _pearsons

    elif matrix_function == "spearman":
        mf = _spearman
        mfs = _spearmans

    elif matrix_function == "polychoric":
        mf = _polychoric
        mfs = _polychorics

        if randomisation_method not in ("shuffle", "bootstrap"):
            raise ValueError(
                (
                    "For polychoric correlations, randomisation method must be shuffle "
                    "or bootstrap."
                )
            )

    elif callable(matrix_function):

        mf = matrix_function

        def mfs(a):
            try:
                with Pool() as pool:
                    results = pool.map(matrix_function, a)

            except AssertionError:
                for _a in tqdm(a):
                    results.append(matrix_function(_a))

            return np.array(results)

    else:
        raise ValueError("Matrix function not recognised.")

    # calculating data eigenvalues
    mat = mf(data)
    eig = _eig(mat, analysis_type)

    # generating random data
    rands = _rands(data, simulations, randomisation_method)

    # calculating random matrices and eigenvalues
    mats = mfs(rands)
    eigs = _eigs(mats, analysis_type)

    # generating criteria
    crit = np.quantile(eigs, quartile, axis=0)

    # applying decision rule
    acc = eig > crit
    factors = np.where(~acc)[0][0]

    if return_figure:
        fig, ax = plt.subplots()
        ax.set_xlabel(f"{'Factor' if analysis_type == 'fa' else 'Component'} number")
        ax.set_ylabel("Eigenvalue")

        x = np.arange(1, eig.size + 1)

        ax.plot(x, eig, label="Observed", color="black", marker="o")
        ax.plot(x, crit, label=f"Threshold", color="red")
        ax.legend()

        return factors, fig  # noqa

    return factors  # noqa
