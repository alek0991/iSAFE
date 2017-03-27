import pandas as pd
import numpy as np
import warnings

def drop_duplicates(snp_matrix, DropDuplicates):

    id, count = np.unique(snp_matrix[0], return_counts=True)
    df = pd.DataFrame(np.asarray([id, count]).T, columns = ["ID", "CopyCount"])
    if df["CopyCount"].max()>1:
        df_drop = df.loc[df["CopyCount"]>1]

        if DropDuplicates:
            print "Dropping %i duplicated ID's (%i distinct ID's)" % (df_drop['CopyCount'].sum(), df_drop.shape[0])
            snp_matrix.drop_duplicates(0, keep=False, inplace=True)
        else:
            warning_text = "%i duplicated ID's (%i distinct ID's) found. You can drop duplicates by setting the flag --DropDuplicates." % (
            df_drop['CopyCount'].sum(), df_drop.shape[0])
            warnings.warn(warning_text)