

import numpy as np



# ========= Error and Rebinning Functions ====================


def autocorr_fft(arr):
    arr = arr - np.mean(arr)
    fft_vals = np.fft.fft(arr)
    spectrum = fft_vals * np.conjugate(fft_vals)
    dest = np.fft.ifft(spectrum)
    return dest / dest[0]


def rebin_array(a, R):
    """Rebin an array into bins of length R"""
    if isinstance(a, list):
        a = np.asarray(a)
    R = int(R)
    max_fit = int(len(a) - len(a) % R)
    if a.ndim == 1:
        # Shape (N): N samples of scalars
        dest = np.mean(a[:max_fit].reshape(-1, R), axis=1)
    elif a.ndim == 2:
        # Shape (N,n,m): N samples of m-dim vecotrs
        N, m = a.shape
        dest = np.mean(a[:max_fit].reshape(-1, m, R), axis=2)
    elif a.ndim == 3:
        # Shape (N,n,m): N samples of n x m matrices
        N, m, n = a.shape
        dest = np.mean(a[:max_fit].reshape(-1, m, n, R), axis=3)
    else:
        print("rebin_array not implemented for dimensions greater than 3.")
        return a
    return dest


def rebin_error(arr):
    """Rebin the given error to avoid autocorrelation in the error estimation

    Args:
        arr (np.ndarray): Timeseries of a measurement

    Returns:
        tuple: (value of binning, mean estimations, error on mean estimations, std dev estimations)
    """
    N = len(arr)
    max_exp = int(np.floor(np.log2(N / 10)))
    rangevals = [2**i for i in range(max_exp + 1)]
    eomarr = []
    stdarr = []
    meanarr = []
    for i in rangevals:
        data_rebin = rebin_array(arr, i)
        eom = np.std(data_rebin, ddof=1) / np.sqrt(len(data_rebin))
        std = np.std(data_rebin, ddof=1)
        eomarr.append(eom)
        meanarr.append(np.mean(data_rebin))
        stdarr.append(std)
    return rangevals, meanarr, eomarr, stdarr


def rebin_eom(arr, num_of_bins=20):
    """Calculate the error on the mean (EOM) by rebinning.
    As a heuristic for the EOM we use that the biggest bin will give the best estimate.
    We do not rebin to the maximal extent, but use the heuristic of taking the largest binsize of the form 2^i that can fit N/20.

    Args:
        arr (np.ndarray): Timeseries of a measurement

    Returns:
        float or arr: Best estimate of the EOM on the given array. The output shape depends on the input shape of arr.
    """
    N = len(arr)
    # We want to leave a sufficient number of samples to build a reasonable mean
    max_exp = int(np.floor(np.log2(N / (num_of_bins / 2))))
    if max_exp > 0:
        binsize = 2 ** (max_exp - 1)
        data_rebin = rebin_array(arr, binsize)
    else:
        # We cannot rebin if we have too few data. We will just return the normal EOM
        data_rebin = arr
    eom = np.std(data_rebin, ddof=1, axis=0) / np.sqrt(len(data_rebin))
    return eom


def autocorr_rebin_eom(arr):
    """Calculate the autocorrelation, and finds the corrrelation decay time (when the auto-correlation decays below 1/100)
    and calculate the error using bins with the correlation time size

    Args:
        arr (np.ndarray): Timeseries of a measurement

    Returns:
        tuple of
            eom: float with the EOM estimation
            decay_time: float with the decay time (in terms of step number) of the autocorrelation
    """
    N = len(arr)
    autocorr_array = autocorr_fft(arr)
    for i in range(len(autocorr_array)):  # find first two elements below 1/100
        if i >= N / 10:  # limit the number of bins to a minimum of 10.
            eom = rebin_eom(arr, 10)
            decay_time = i
            return eom, decay_time
        elif autocorr_array[i] <= 1 / 100 and autocorr_array[i + 1] <= 1 / 100:
            num_of_bins = N // i
            eom = rebin_eom(arr, num_of_bins)
            decay_time = i
            return eom, decay_time


def autocorr_rebin_data(arr):
    """
    Rebin the data to remove autocorrelation.
    The binsize is determined by the first two elements of the autocorrelation function that are below 1/100.

    Args:
        arr (np.ndarray): Timeseries of a measurement
    Returns:
        np.ndarray: Rebinend data
    """
    N = len(arr)
    autocorr_array = autocorr_fft(arr)
    for i in range(len(autocorr_array)):  # find first two elements below 1/100
        if i >= N / 10:  # limit the number of binsto a minimum of 10.
            binsize = i
            break
        elif autocorr_array[i] <= 1 / 100 and autocorr_array[i + 1] <= 1 / 100:
            binsize = i
            break
    rebinned_array = rebin_array(arr, binsize)
    return rebinned_array, binsize


def jackknife_resampling(data):
    """Generate jackknife resamples of the data."""
    n = len(data)
    indices = np.arange(n)
    resamples = np.zeros(n)
    for i in range(n):
        resamples[i] = np.mean(data[indices != i])
    return resamples


def jacknife_gradient_error_propagation(op_datavec, op_grad_datavec, grad_norm_datavec):
    """Calculate the error propagation of the gradient of an observable using jackknife resampling.

    Args:
        op_datavec (np.ndarray): Timeseries of the observable - rebinned data, i.e., not autocorrelation
        op_grad_datavec (np.ndarray): Timeseries of the gradient of the observable - rebinned data, i.e., not autocorrelation
        grad_norm_datavec (np.ndarray): Timeseries of the gradient of the norm of the ansatz divided by the norm of the ansatz
        - rebinned data, i.e., not autocorrelation

    Returns:
        float: Error of the gradient of the observable
    """
    op_datavec_resamples = jackknife_resampling(op_datavec)
    op_grad_datavec_resamples = jackknife_resampling(op_grad_datavec)
    grad_norm_datavec_resamples = jackknife_resampling(grad_norm_datavec)
    op_times_grad_norm_resamples = jackknife_resampling(op_datavec * grad_norm_datavec)
    mean_grad = np.mean(
        op_grad_datavec_resamples
        + op_times_grad_norm_resamples
        - op_datavec_resamples * grad_norm_datavec_resamples
    )
    grad_jacknife = (
        op_grad_datavec_resamples
        + op_times_grad_norm_resamples
        - op_datavec_resamples * grad_norm_datavec_resamples
    )
    n = len(grad_jacknife)

    return np.sqrt((n - 1) * np.mean((grad_jacknife - mean_grad) ** 2))


def compute_grad_err(op_datavec, op_grad_datavec, grad_norm_datavec):
    """Compute the error of the gradient of an observable.

    Args:
        op_datavec(np.ndarray): Timeseries of the observable
        op_grad_datavec(np.ndarray): Timeseries of the gradient of the observable
        grad_norm_datavec(np.ndarray): Timeseries of the gradient of the norm of the ansatz divided by the norm of the ansatz
    Returns:
        float: Error of the gradient of the observable
    """
    op_datavec_rebinned, op_datavec_rebinned_binsize = autocorr_rebin_data(op_datavec)
    op_grad_datavec_rebinned, op_grad_datavec_rebinned_binsize = autocorr_rebin_data(
        op_grad_datavec
    )
    grad_norm_datavec_rebinned, grad_norm_datavec_rebinned_binsize = (
        autocorr_rebin_data(grad_norm_datavec)
    )
    max_binsize = max(
        op_datavec_rebinned_binsize,
        op_grad_datavec_rebinned_binsize,
        grad_norm_datavec_rebinned_binsize,
    )

    if (
        max_binsize > op_datavec_rebinned_binsize
    ):  # All arrays should be of the same size, so we pick the largest binsize
        op_datavec_rebinned = rebin_array(op_datavec, max_binsize)
    if max_binsize > op_grad_datavec_rebinned_binsize:
        op_grad_datavec_rebinned = rebin_array(op_grad_datavec, max_binsize)
    if max_binsize > grad_norm_datavec_rebinned_binsize:
        grad_norm_datavec_rebinned = rebin_array(
            grad_norm_datavec,
            max_binsize,
        )
    return jacknife_gradient_error_propagation(
        op_datavec_rebinned, op_grad_datavec_rebinned, grad_norm_datavec_rebinned
    )


def compute_grad_mean(op_datavec, op_grad_datavec, grad_norm_datavec):
    """Compute the mean of the gradient of an observable.

    Args:
        op_datavec(np.ndarray): Timeseries of the observable
        op_grad_datavec(np.ndarray): Timeseries of the gradient of the observable
        grad_norm_datavec(np.ndarray): Timeseries of the gradient of the norm of the ansatz divided by the norm of the ansatz
    Returns:
        float: Mean of the gradient of the observable
    """
    mean = np.mean(op_grad_datavec + op_datavec * grad_norm_datavec)
    mean = mean - np.mean(op_datavec) * np.mean(grad_norm_datavec)
    return mean


