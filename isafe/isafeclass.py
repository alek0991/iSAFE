import numpy as np
import pandas as pd
import sys
from .safeclass import SafeClass

def create_rolling_indices(total_variant_count, w_size, w_step):
    if total_variant_count<w_size:
        raise ValueError('Total number of variants (%i) cannot be smaller than sliding window size (--window %i). Please carefully read the instruction for following arguments: --SAFE, --window, --step, --MinRegionSize-bp, and --MinRegionSize-ps'%(total_variant_count, w_size))
    if w_step <= 0:
        return
    w_start = 0
    rolling_indices = []
    while True:
        w_end = min(w_start + w_size, total_variant_count)
        if w_end >= total_variant_count:
            break
        rolling_indices += [list(range(int(w_start), int(w_end)))]
        w_start += w_step
    return rolling_indices


def creat_windows_summary_stats(snp_matrix, w_size, w_step, step_counter='XX', status=True):
    total_variant_count = snp_matrix.shape[0]
    rolling_indices = create_rolling_indices(total_variant_count, w_size, w_step)
    windows_stats = {}
    progress0 = 0
    for i, I in enumerate(rolling_indices):
        progress = np.round(100.0 * i / len(rolling_indices))
        if (progress>progress0):
            if status:
                sys.stdout.write("\r\tStep %s: %.2i%%" % (step_counter, progress))
                sys.stdout.flush()
            progress0 = progress

        window_i_stats = {}
        df = snp_matrix.iloc[I]
        snp_matrix_i = df.values.T
        obj_safe = SafeClass(snp_matrix_i)
        window_i_stats["safe"] = obj_safe.creat_dataframe()
        window_i_stats["safe"]["pos"] = df.index
        window_i_stats["safe"]["ordinal_pos"] = I
        window_i_stats["haf"] = obj_safe.haf
        windows_stats[i] = window_i_stats
    return windows_stats


def creat_snps_information_df(WS):
    """
    :param WS:Reads df of each window and concatenates them.
    :return:
    """
    temp_list = []
    for key in list(WS.keys()):
        dfi = WS[key]["safe"].loc[:, ["ordinal_pos", "pos", "safe", "rank", "freq"]]
        dfi["window"] = key
        temp_list += [dfi]
    return pd.concat(temp_list).reset_index(drop=True)

def get_top_k_snps_in_each_window(df_snps, k=1):
    """
    :param df_snps:  this datafram must have following columns: ["safe","ordinal_pos","window"].
    :param k:
    :return: return top k snps in each window.
    """
    return df_snps.loc[df_snps.groupby('window')['safe'].nlargest(k).index.get_level_values(1), :].reset_index(drop=True)

def isafe_kernel(haf, snp):
    phi = haf[snp == 1].sum() * 1.0 / haf.sum()
    kappa = len(np.unique(haf[snp == 1])) / (1.0 * len(np.unique(haf)))
    f = np.mean(snp)
    sigma2 = (f) * (1 - f)
    if sigma2 == 0:
        sigma2 = 1.0
    sigma = sigma2 ** 0.5
    p = (phi - kappa) / sigma
    return p

def creat_matrix_Psi_k(M, Dw, Ifp, step_counter='XX', status=True):
    P = np.zeros((len(Ifp), len(Dw)))
    progress0 = 0
    for i in range(len(Ifp)):
        progress = np.round(100.0 * i / len(Ifp))
        if (progress>progress0):
            if status:
                sys.stdout.write("\r\tStep %s: %.2i%%" % (step_counter, progress))
                sys.stdout.flush()
            progress0 = progress
        for j in list(Dw.keys()):
            output = isafe_kernel(Dw[j]["haf"], M[:, Ifp[i]])
            P[i, j] = output
    return step_function(P)

def step_function(P0):
    P = P0.copy()
    P[P < 0] = 0
    return P

# def apply_isafe(snp_matrix, w_size, w_step, top_k1, top_k2, status = False):
#     if status:
#         toolbar_width = 4
#         sys.stdout.write("[%s]" % (" " * toolbar_width))
#         sys.stdout.flush()
#         sys.stdout.write("\b" * (toolbar_width + 1))
#         sys.stdout.write("-")
#         sys.stdout.flush()
#     WS = creat_windows_summary_stats(snp_matrix, w_size, w_stepcreat_windows_summary_stats)
#     if status:
#         sys.stdout.write("-")
#         sys.stdout.flush()
#     df_snps = creat_snps_information_df(WS)
#     df_top_k1 = get_top_k_snps_in_each_window(df_snps, k=top_k1)
#     cand_snp_k1 = np.sort(df_top_k1["ordinal_pos"].unique())
#     Psi_k1 = creat_matrix_Psi_k(snp_matrix.values.T, WS, cand_snp_k1)
#     if status:
#         sys.stdout.write("-")
#         sys.stdout.flush()
#     df_top_k2 = get_top_k_snps_in_each_window(df_snps, k=top_k2)
#     temp = np.sort(df_top_k2["ordinal_pos"].unique())
#     cand_snp_k2 = np.sort(np.setdiff1d(temp, cand_snp_k1))
#     Psi_k2 = creat_matrix_Psi_k(snp_matrix.values.T, WS, cand_snp_k2)
#     if status:
#         sys.stdout.write("-")
#         sys.stdout.flush()
#
#
#     alpha = Psi_k1.sum(0) / Psi_k1.sum()
#
#     iSAFE1 = pd.DataFrame(data={"ordinal_pos": cand_snp_k1, "isafe": np.dot(Psi_k1, alpha)})
#     iSAFE2 = pd.DataFrame(data={"ordinal_pos": cand_snp_k2, "isafe": np.dot(Psi_k2, alpha)})
#
#     iSAFE1["tier"] = 1
#     iSAFE2["tier"] = 2
#     iSAFE = pd.concat([iSAFE1, iSAFE2]).reset_index(drop=True)
#     iSAFE["id"] = snp_matrix.iloc[iSAFE["ordinal_pos"]].index
#     freq = snp_matrix.mean(1).values.squeeze()
#     iSAFE["freq"] = freq[iSAFE["ordinal_pos"].values.squeeze()]
#     if status:
#         sys.stdout.write("\niSAFE Done!\n")
#     return iSAFE[["ordinal_pos", "id", "isafe", "freq", "tier"]], Psi_k1

class iSafeClass:
    def __init__(self, snp_matrix, w_size, w_step, top_k1, top_k2):
        self.snp_matrix = snp_matrix
        self.w_size = w_size
        self.w_step = w_step
        self.top_k1 = top_k1
        self.top_k2 = top_k2
        self.windows_summary = None
        self.snps_summary = None
        self.psi_k1 = None
        self.psi_k2 = None
        self.ordinal_pos_snps_k1 = None
        self.ordinal_pos_snps_k2 = None
        self.alpha = None
        self.isafe = None

    def fire(self, status=True):
        step_counter = '1/3'
        if status:
            sys.stdout.write("Data loaded successfully.\nRunning iSAFE:\n")
        self.windows_summary = creat_windows_summary_stats(self.snp_matrix, self.w_size, self.w_step, step_counter=step_counter,  status=status)
        if status:
            sys.stdout.write("\r\tStep %s: 100%%\n"%(step_counter))
            sys.stdout.flush()
        self.snps_summary = creat_snps_information_df(self.windows_summary)
        df_top_k1 = get_top_k_snps_in_each_window(self.snps_summary, k=self.top_k1)
        self.ordinal_pos_snps_k1 = np.sort(df_top_k1["ordinal_pos"].unique())
        step_counter = '2/3'
        self.psi_k1 = creat_matrix_Psi_k(self.snp_matrix.values.T, self.windows_summary, self.ordinal_pos_snps_k1, step_counter=step_counter,  status=status)
        if status:
            sys.stdout.write("\r\tStep %s: 100%%\n"%step_counter)
            sys.stdout.flush()
        df_top_k2 = get_top_k_snps_in_each_window(self.snps_summary, k=self.top_k2)
        temp = np.sort(df_top_k2["ordinal_pos"].unique())
        self.ordinal_pos_snps_k2 = np.sort(np.setdiff1d(temp, self.ordinal_pos_snps_k1))
        step_counter = '3/3'
        self.psi_k2 = creat_matrix_Psi_k(self.snp_matrix.values.T, self.windows_summary, self.ordinal_pos_snps_k2, step_counter=step_counter, status=status)
        if status:
            sys.stdout.write("\r\tStep %s: 100%%\n" % step_counter)
            sys.stdout.flush()

        self.alpha = self.psi_k1.sum(0) / self.psi_k1.sum()

        iSAFE1 = pd.DataFrame(data={"ordinal_pos": self.ordinal_pos_snps_k1, "isafe": np.dot(self.psi_k1, self.alpha)})
        iSAFE2 = pd.DataFrame(data={"ordinal_pos": self.ordinal_pos_snps_k2, "isafe": np.dot(self.psi_k2, self.alpha)})

        iSAFE1["tier"] = 1
        iSAFE2["tier"] = 2
        iSAFE = pd.concat([iSAFE1, iSAFE2]).reset_index(drop=True)
        iSAFE["id"] = self.snp_matrix.iloc[iSAFE["ordinal_pos"]].index
        freq = self.snp_matrix.mean(1).values.squeeze()
        iSAFE["freq"] = freq[iSAFE["ordinal_pos"].values.squeeze()]
        if status:
            sys.stdout.write("iSAFE completed successfully.\n")
        self.isafe = iSAFE[["ordinal_pos", "id", "isafe", "freq", "tier"]]

    def creat_psi_k1_dataframe(self):
        df = pd.DataFrame(self.psi_k1, index = self.snp_matrix.iloc[self.ordinal_pos_snps_k1].index.tolist(),
                            columns=["w%i"%x for x in range(1,self.psi_k1.shape[1]+1)])
        df.index.rename("#SnpID", inplace=True)
        return df
