import numpy as np #Need numpy version 1.9 or above
import pandas as pd


###################################################################################################
def HAF(M):
    """
    :type M: Binary SNP Matrix, Columns are mutations
    :return HAF-score: (n,) int array
    """
    return np.dot(M, M.T).sum(1)


###################################################################################################
def calc_H_K(M):
    """
    :param M: Binary SNP Matrix
    :return: H: Sum of HAF-score of carriers of each mutation.
    :return: N: Number of distinct carrier haplotypes of each mutation.

    """
    haf_scores = HAF(M)
    haf_matrix = haf_scores.reshape(-1, 1) * M
    N = np.zeros((M.shape[1]))
    for j in range(M.shape[1]):
        ar = haf_matrix[:, j]
        N[j] = len(np.unique(ar[ar > 0])) #Need numpy version 1.9 or above
    H = np.sum(haf_matrix, 0)
    return H, N

###################################################################################################

def neutrality_divergence_proxy(h, n, f, method=2):
    if method == 1:
        sigma2 = (n) * (1 - n)
        sigma2[sigma2 == 0] = 1.0
        sigma = sigma2 ** 0.5
        p = (h - n) / sigma
    elif method ==2:
        sigma2 = (f) * (1 - f)
        sigma2[sigma2 == 0] = 1.0
        sigma = sigma2 ** 0.5
        p = (h - n) / sigma
    elif method == 3:
        p1 = neutrality_divergence_proxy(h, n, f, 1)
        nu = f[np.argmax(p1)]
        p2 = neutrality_divergence_proxy(h, n, f, 2)
        p = p1*(1-nu)+p2*nu
    return p
####################################################################################################

def apply_safe(M):
    [H, K] = calc_H_K(M)
    haf = HAF(M)
    phi = 1.0 * H / sum(haf)
    kappa = 1.0 * K / (np.unique(haf).shape[0])
    freq = M.mean(0)
    safe = neutrality_divergence_proxy(phi, kappa, freq, method=3)
    rank = pd.DataFrame(safe).rank(method = 'min', ascending=False).values.squeeze()
    df_safe = pd.DataFrame(np.asarray([safe, rank, phi, kappa, freq]).T, columns=["safe", "rank", "phi", "kappa", "freq"])
    return df_safe