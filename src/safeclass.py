import numpy as np #Need numpy version 1.9 or above
import pandas as pd


class SafeClass:

    def __init__(self, M):
        self.snp_matrix = M
        self.haf = self.HAF()
        self.num_snps = M.shape[1]
        self.num_haplotypes = M.shape[0]
        self.H, self.K = self.calc_H_K()
        self.phi = 1.0 * self.H / sum(self.haf)
        self.kappa = 1.0 * self.K / (np.unique(self.haf).shape[0])
        self.freq = M.mean(0)
        self.safe = self.neutrality_divergence_proxy()
        self.rank = pd.DataFrame(self.safe).rank(method='min', ascending=False).values.squeeze()
    ###################################################################################################
    def HAF(self):
        """
        :type snp_matrix: Binary SNP Matrix, Columns are mutations
        :return haf: HAF-score, (n,) int array
        """
        return np.dot(self.snp_matrix, self.snp_matrix.T).sum(1)
    ###################################################################################################
    def calc_H_K(self):
        """
        :param snp_matrix: Binary SNP Matrix
        :return: H: Sum of HAF-score of carriers of each mutation.
        :return: N: Number of distinct carrier haplotypes of each mutation.

        """
        
        haf_matrix = self.haf.reshape(-1, 1) * self.snp_matrix
        K = np.zeros((self.num_snps))
        for j in range(self.num_snps):
            ar = haf_matrix[:, j]
            K[j] = len(np.unique(ar[ar > 0])) #Need numpy version 1.9 or above
        H = np.sum(haf_matrix, 0)
        return H, K

    ###################################################################################################

    def neutrality_divergence_proxy(self, method=3):
        if method == 1:
            sigma2 = (self.kappa) * (1 - self.kappa)
            sigma2[sigma2 == 0] = 1.0
            sigma = sigma2 ** 0.5
            p = (self.phi - self.kappa) / sigma
        elif method ==2:
            sigma2 = (self.freq) * (1 - self.freq)
            sigma2[sigma2 == 0] = 1.0
            sigma = sigma2 ** 0.5
            p = (self.phi - self.kappa) / sigma
        elif method == 3:
            p1 = self.neutrality_divergence_proxy(1)
            nu = self.freq[np.argmax(p1)]
            p2 = self.neutrality_divergence_proxy(2)
            p = p1*(1-nu)+p2*nu
        return p
    ####################################################################################################
    def creat_dataframe(self):
        df_safe = pd.DataFrame(np.asarray([self.safe, self.rank, self.phi, self.kappa, self.freq]).T, columns=["safe", "rank", "phi", "kappa", "freq"])
        return df_safe