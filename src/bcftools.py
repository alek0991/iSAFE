import numpy as np
import pandas as pd
import os
from StringIO import StringIO
import warnings
bcf_tools = "bcftools"

def get_sample_IDs(the_vcf):
    cmd = "%s query -l %s"%(bcf_tools, the_vcf)
    return os.popen(cmd).read().split()


def get_ploidy(target_region, sample_arg, the_vcf):
    cmd = "%s view" % bcf_tools
    cmd += " -r %s" % target_region
    cmd += sample_arg
    cmd += " -i 'N_ALT==1'"
    cmd += " %s" % (the_vcf)
    cmd += " | %s plugin check-ploidy"%bcf_tools
    dfp = pd.read_csv(StringIO(os.popen(cmd).read()), sep='\t')
    dfp.columns = ['Sample', 'Chromosome', 'Region Start', 'Region End', 'Ploidy']
    id, count = np.unique(dfp['Sample'], return_counts=True)
    mixed_ploidy_samples = id[count > 1]
    if len(mixed_ploidy_samples)>0:
        raise ImportError("Ploidy inconsistency error (haploid and diploid sites together in a sample): Mixed ploidy in samples %s"%mixed_ploidy_samples)
    else:
        return dfp.set_index('Sample')['Ploidy']

def load_vcf_as_df(the_vcf, chrom, region_start, region_end, samples=None):
    if samples == []:
        samples = None
    if samples is None:
        sample_arg = ""
        sample_IDs = get_sample_IDs(the_vcf)
    else:
        sample_arg = " -s %s" % (','.join(str(x) for x in samples))
        sample_IDs = samples

    target_region = "%s:%i-%i" % (chrom, region_start, region_end)
    ploidy = get_ploidy(target_region, sample_arg, the_vcf)

    cmd = "%s query" % bcf_tools
    cmd += " -r %s" % target_region
    cmd += sample_arg
    # cmd += " -i 'TYPE=\"snp\" && N_ALT==1'" # remove not SNPs (indels, MNPs, and etc) and remove variants with more than 1 ALT.
    cmd += " -i 'N_ALT==1'" # keeps SNPs and not SNPs (indels, MNPs, and etc) as long as they have only 1 ALT.
    # cmd += " -i 'TYPE=\"snp\"'"
    cmd += " -f '%CHROM\\t%POS\\t%ID\\t%REF\\t%ALT[\\t%GT]\\n'"
    cmd += " %s" % (the_vcf)
    cmd += " | tr '|' '\\t'"
    try:
        df = pd.read_csv(StringIO(os.popen(cmd).read()), sep='\t', header=None)
    except pd.io.common.EmptyDataError:
        raise ImportError("There are no variants in the target region %s!"%target_region)

    Alleles = np.unique(["%s" % x for x in np.unique(df.iloc[:, 5:].values.reshape(-1))])

    if len(np.setdiff1d(Alleles, ['0', '1']))>0:
        raise ImportError("Input is not biallelic (0 and 1). Allele set = %s"%Alleles)

    header = ["CHROM", "POS", "ID", "REF", "ALT"]
    for i, id in enumerate(sample_IDs):
        header += [id]*ploidy.loc[id]
    df.columns = header
    return df,sample_IDs


def get_combined_vcf(chrom, region_start, region_end, case_vcf, cont_vcf=None, case_IDs=None, cont_IDs=None):
    if cont_vcf is None:
        if case_IDs is None:
            samples = None
            df, sample_IDs = load_vcf_as_df(case_vcf, chrom, region_start, region_end, samples=samples)
            IDmap = pd.DataFrame([['target'] * len(sample_IDs), sample_IDs, ['case'] * len(sample_IDs)]).T
            IDmap.columns = ['pop', 'sample', 'group']
        else:
            samples = case_IDs['sample'].tolist()
            df, sample_IDs = load_vcf_as_df(case_vcf, chrom, region_start, region_end, samples=samples)
            IDmap = case_IDs
    elif case_vcf == cont_vcf:
        IDmap = pd.concat([case_IDs, cont_IDs])
        the_vcf = case_vcf
        samples = IDmap['sample'].tolist()
        if len(samples)> len(np.unique(samples)):
            raise ValueError("--sample-case and/or --sample-cont have shared/duplicated samples.")
        df, _ = load_vcf_as_df(the_vcf, chrom, region_start, region_end, samples=samples)
    else:
        if case_IDs is None:
            samples = None
            df, sample_IDs = load_vcf_as_df(case_vcf, chrom, region_start, region_end, samples=samples)
            case_IDs = pd.DataFrame([['target'] * len(sample_IDs), sample_IDs, ['case'] * len(sample_IDs)]).T
            case_IDs.columns = ['pop', 'sample', 'group']
        else:
            samples = case_IDs['sample'].tolist()
            df, sample_IDs = load_vcf_as_df(case_vcf, chrom, region_start, region_end, samples=samples)
        df1 = df.copy(deep=True)
        if cont_IDs is None:
            samples = None
            df, sample_IDs = load_vcf_as_df(cont_vcf, chrom, region_start, region_end, samples=samples)
            cont_IDs = pd.DataFrame([['nontarget'] * len(sample_IDs), sample_IDs, ['cont'] * len(sample_IDs)]).T
            cont_IDs.columns = ['pop', 'sample', 'group']
        else:
            samples = cont_IDs['sample'].tolist()
            df, sample_IDs = load_vcf_as_df(cont_vcf, chrom, region_start, region_end, samples=samples)
        df2 = df.copy(deep=True)
        IDmap = pd.concat([case_IDs, cont_IDs])
        df = pd.merge(df1, df2, how='inner', on=["CHROM", "POS", "REF", "ALT"], suffixes=("", "2"))
        del df['ID2']

    df = df.set_index(["CHROM", "POS", "ID", "REF", "ALT"])
    cols = []
    xl = []
    for x in df.columns:
        temp = list(IDmap.loc[IDmap['sample'] == x, ["group", "pop", "sample"]].values.squeeze())
        if x in xl:
            hap = 'B'
        else:
            hap = 'A'
        cols += [tuple(temp + [hap])]
        xl += [x]
    df.columns = pd.MultiIndex.from_tuples(cols, names=['group', 'pop', 'sample', 'hap'])
    return df

def get_AA_df(AA_file, df):
    POS = df.index.get_level_values("POS").tolist()
    f= open(AA_file,'r')
    l=f.readline()
    ref_ch=f.read().replace("\n","").upper()
    # ref_ch=f.read().replace("\n","")
    f.close()
    AA = []
    for pos in POS:
        AA += [ref_ch[pos - 1]]
    dfAA = pd.DataFrame([POS,AA]).T
    dfAA.columns=["POS", "AA"]
    dfAA['POS'] = dfAA['POS'].astype(int)
    df2 = df.iloc[:,[0,1]]
    df2.columns=[0,1]
    df2 = df2.reset_index()
    del df2[0]
    del df2[1]
    dfI = pd.merge(df2, dfAA, how='left', on='POS')
    dfI['FLIP'] = False
    dfI.loc[dfI["ALT"]==dfI['AA'], "FLIP"] = True
    return dfI

def get_snp_matrix(chrom, region_start, region_end, case_vcf, AA_file, cont_vcf=None, sample_case=None, sample_cont=None,RandomSampleRate=0.1,ForceRandomSample=False, status=False):
    if sample_case is not None:
        case_IDs = pd.read_csv(sample_case, sep='\t', header=None, comment='#').rename(columns={0: "pop", 1: "sample"})
        case_IDs["group"] = 'case'
    else:
        case_IDs = None

    if sample_cont is not None:
        cont_IDs = pd.read_csv(sample_cont, sep='\t', header=None, comment='#').rename(columns={0: "pop", 1: "sample"})
        cont_IDs["group"] = 'cont'
    else:
        cont_IDs = None

    total_window_size=region_end-region_start
    if status:
        print 'Loading %0.3fMbp, %s:%i-%i, please wait ...'%(total_window_size/1e6, chrom, region_start, region_end)
    df = get_combined_vcf(chrom, region_start, region_end, case_vcf, cont_vcf=cont_vcf, case_IDs=case_IDs, cont_IDs=cont_IDs)
    dfI = get_AA_df(AA_file, df)
    I = df.index.get_level_values("POS").isin(dfI.loc[dfI['FLIP']==True, "POS"])
    df.loc[I, :]=1-df.loc[I, :]
    dfreq = df.groupby(level=0, axis=1).mean().join(df.groupby(level=1, axis=1).mean())
    dfreq['MDDAF'] = dfreq['case']-dfreq.min(1)
    Need_Random_Sample = sum((dfreq['case']>0.9)&(dfreq['MDDAF']>0.78))>0
    I = df.columns.get_level_values("group").isin(['case'])
    if Need_Random_Sample | ForceRandomSample:
        case_num = sum(df.columns.get_level_values("group")=='case')
        NumberRandomSample = int(np.round(RandomSampleRate/(1-RandomSampleRate)*case_num))
        if status:
            print "Adding %i random haplotypes (%i%%)." % (NumberRandomSample, RandomSampleRate * 100)
        I1 = list(np.random.choice(np.where(I==False)[0], NumberRandomSample))

        I[I1] = True
    elif cont_vcf is not None:
        if status:
            print "MDDAF: Random samples are not required."
    return df.loc[:,I], dfreq, dfI,Need_Random_Sample
