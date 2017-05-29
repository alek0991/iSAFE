import argparse
import warnings
import pandas as pd
from isafeclass import iSafeClass
from utils import *
from bcftools import get_snp_matrix
def run():
    # command line parser
    parser = argparse.ArgumentParser(description='===================================================================='
                                                 '\niSAFE: (i)ntegrated (S)election of (A)llele (F)avored by (E)volution'
                                                 '\n===================================================================='
                                                 '\nSource code can be found at: <https://github.com/alek0991/iSAFE>'
                                                 '\niSAFE v0.0.0'
                                                 '\n--------------------------------------------------------------------', formatter_class=argparse.RawTextHelpFormatter)

    # optional arguments
    parser.add_argument('--format', '-f',help='<string>: Input format. '
                                              '<FORMAT> must be either hap or vcf (see the manual for more details).'
                                              '\nNOTE 1: vcf format can handle both vcf.gz (.tbi file is required for bcftools) and vcf.'
                                              '\nNOTE 2: When input format is vcf, Ancestral Allele file (--AA) must be given.'
                                              '\nNOTE 3: Input with hap format is not allowed with any of these: --vcf-cont, --sample-case, --sample-cont, --AA.'
                                              '\nNOTE 4: When the input format is hap, iSAFE assumes that derived allele is 1 and ancestral allele is 0 in the input file, '
                                              '\nand the selection is ongoing (favored mutation is not fixed).'
                                              '\nDefault: vcf', required=False, default='vcf')
    parser.add_argument('--input', '-i',help='<string>: Path to input.', required=True)
    parser.add_argument('--output', '-o',help='<string>: Path to output.'
                                              '\nNOTE 1: iSAFE generates <OUTPUT>.iSAFE.out'
                                              '\nNOTE 2: When --OutputPsi is set, iSAFE generates <OUTPUT>.Psi.out in addition to <OUTPUT>.iSAFE.out'
                        , required=True)

    parser.add_argument('--vcf-cont', help='<string>: Path to the phased control population in .vcf or .vcf.gz format.', required=False)
    parser.add_argument('--sample-case', help='<string>: Path to the samples file of the case population.'
                                              '\nNOTE 1: This option is only available in --format vcf.'
                                              '\nNOTE 2: This file must have two columns, the first one is population and the second column is sample ID\'s used in the --input.'
                                              '\nNOTE 3: When this option is not used all the samples in the --input are considered as the case samples.'
                                              '\nNOTE 4 Must use this when case and control populations are in the same vcf file.'
                                              '\nNOTE 5: This file must be TAB separated, no header, and comments by #.'
                                              '\nNOTE 6: Population column (first column) can have more than one population name. They are all considered the CASE populations.'
                                              '\nNOTE 7: You can use whatever name you want for populations, but sample ID\'s must be in --input vcf file', required=False)
    parser.add_argument('--sample-cont', help='<string>: Path to the samples file of the control populations. These TAB separated file must have two columns, the first one is population name and the second column is sample ID\'s used in the --vcf-cont'
                                              '\nNOTE: When this option is not used all the samples in the --input is considered as the case samples.', required=False)
    parser.add_argument('--AA', help='<string>: Path to the Ancestral Allele (AA) file in FASTA (.fa) format (see the manual for details)', required=False)
    parser.add_argument('--region', help='<chr:string>:<start position:int>-<end position:int>, the coordinates of the target region in the genome.'
                                         '\nExamples, 2:10000000-15000000 or 2:10,000,000-15,000,000. '
                                         '\nNOTE 1: The <chr> is dumped when the input is --hap.'
                                         '\nNOTE 2: <chr> format (e.g. chr2 or 2) must be consistent with vcf files.', required=False)

    parser.add_argument('--MaxRegionSize', type=int, help='<int>: Maximum region size in bp.\nDefault: 6000000', required=False, default=6000000)
    parser.add_argument('--MaxGapSize', type=int, help='<int>: Maximum gap size in bp.\nDefault: 10000', required=False, default=10e3)
    parser.add_argument('--window', type=int, help='<int>: Sliding window size in polymorphic sites.\nDefault: 300', required=False, default=300)
    parser.add_argument('--step', type=int, help='<int>: Step size of sliding window in polymorphic sites.\nDefault: 150', required=False, default=150)
    parser.add_argument('--topk', type=int, help='<int>: Rank of SNPs used for learning window weights (alpha).\nDefault: 1', required=False, default=1)
    parser.add_argument('--MaxRank', type=int, help='<int>: Ignore SNPs with rank higher than MAXRANK.\nNOTE: For considering all SNPs set --MaxRank > --window (Default: 300).\nDefault: 15', required=False, default=15)
    parser.add_argument('--MaxFreq', type=float, help='<float>: Ignore SNPs with frequency higher than MAXFreq.\nDefault: 0.95',
                        required=False, default=0.95)
    parser.add_argument('--RandomSampleRate', type=float, help='<float>: Portion of added random samples.'
                                                               '\nNOTE 1: RandomSampleRate = RandomSamples/(RandomSamples+CaseSamples).'
                                                               '\nNOTE 2: Must be non-negative and less than 1.\nDefault: 0.1',
                        required=False, default=0.1)
    parser.add_argument('--ForceRandomSample', '-FRS', help='<bool>: Set this flag to force the iSAFE to use random samples even when MDDAF does not suggest.\nNOTE: --vcf-cont must be provided.\nDefault: false', action='store_true')
    parser.add_argument('--IgnoreGaps', '-IG', help='<bool>: Set this flag to ignore gaps.\nDefault: false', action='store_true')
    parser.add_argument('--StatusOff', '-SO', help='<bool>: Set this flag to turn off printing status.\nDefault: false', action='store_true')
    parser.add_argument('--OutputPsi', '-Psi', help='<bool>: Set this flag to output Psi_1 in a text file with suffix .Psi.out.\nDefault: false', action='store_true')
    args = parser.parse_args()

    if (args.format not in ['hap', 'vcf']):
        raise ValueError("--format must be either hap or vcf.")
    if (args.format == 'hap'):
        if ((args.vcf_cont is not None)|(args.sample_case is not None)|(args.sample_cont is not None)|(args.AA is not None)):
            parser.error("[--format hap] is not allowed with any of these: --vcf-cont, --sample-case, --sample-cont, --AA.")
        else:
            warnings.warn("With [--format hap], iSAFE assumes that derived allele is 1 and ancestral allele is 0 in the input file, and the selection is ongoing (the favored mutation is not fixed).")
    if (args.format == 'vcf'):
        if args.AA is None:
            parser.error("--AA must be provided when input format is vcf.")
        if args.region is None:
            parser.error("--region must be provided when input format is vcf.")
        elif args.input == args.vcf_cont:
            if (args.sample_case is None)|(args.sample_cont is None):
                parser.error("--sample-case and --sample-cont must be provided when --input and --vcf-cont are the same.")
        if args.vcf_cont is None:
            if args.ForceRandomSample:
                parser.error("--ForceRandomSample needs --vcf-cont.")
        if (args.RandomSampleRate>=1)|(args.RandomSampleRate<0):
            raise ValueError("--RandomSampleRate must be non-negative and less than 1.")
    status = not args.StatusOff
    if args.region is not None:
        try:
            chrom, region_start, region_end = parse_region(args.region.replace(',', ''))
        except:
            raise ValueError("--region must be in this format: chr:start-end, e.g. 2:10000000-15000000 or 2:10,000,000-15,000,000")
        total_window_size = region_end-region_start
        if total_window_size>args.MaxRegionSize:
            raise ValueError("Error: The region is %.3fMbp and it cannot be greater than %iMbp."%(total_window_size/1e6, args.MaxRegionSize/1e6))

    if args.format == 'vcf':
        df, dfreq, dfI, Need_Random_Sample = get_snp_matrix(chrom, region_start, region_end, args.input, args.AA,
                                                            cont_vcf=args.vcf_cont, sample_case=args.sample_case, sample_cont=args.sample_cont,
                                                            RandomSampleRate=args.RandomSampleRate,
                                                            ForceRandomSample=args.ForceRandomSample, status=status)
        snp_matrix = pd.DataFrame(df.values)
        snp_matrix.index = df.index.get_level_values("POS")
    else:
        snp_matrix = pd.read_csv(args.input, sep="\t", header=None, comment='#')
        snp_matrix.set_index(0, inplace=True)
        if args.region is not None:
            I = (snp_matrix.index>=region_start) & (snp_matrix.index<=region_end)
            snp_matrix=snp_matrix.loc[I]
    POS = np.asarray(snp_matrix.index)
    total_window_size = POS.max() - POS.min()
    dp = np.diff(POS)
    num_gaps = sum(dp>args.MaxGapSize)
    if total_window_size>args.MaxRegionSize:
        raise ValueError("The region is %.3fMbp and it cannot be greater than %iMbp." % (
        total_window_size / 1e6, args.MaxRegionSize / 1e6))

    if num_gaps>0:
        if not args.IgnoreGaps:
            raise ValueError("There is %i gaps with size greater than %ikbp."%(num_gaps, args.MaxGapSize/1e3))
        else:
            if status:
                warnings.warn("Warning: There is %i gaps with size greater than %ikbp." % (num_gaps, args.MaxGapSize/ 1e3))
    f = snp_matrix.mean(1)
    snp_matrix = snp_matrix.loc[((1 - f) * f) > 0]
    if status:
        print "%i SNPs and %i Haplotypes" % (snp_matrix.shape[0], snp_matrix.shape[1])
    obj_isafe = iSafeClass(snp_matrix, args.window, args.step, args.topk, args.MaxRank)
    obj_isafe.fire(status=status)
    df_final = obj_isafe.isafe.loc[obj_isafe.isafe["freq"]<args.MaxFreq].sort_values("ordinal_pos").rename(columns={'id':"POS", 'isafe':'iSAFE', "freq":"DAF"})
    df_final[["POS", "iSAFE", "DAF"]].to_csv("%s.iSAFE.out"%args.output, index=None,sep='\t')
    if args.OutputPsi:
        psi_k1 = obj_isafe.creat_psi_k1_dataframe()
        psi_k1.index.rename("#POS", inplace=True)
        psi_k1.to_csv("%s.Psi.out"%args.output, sep='\t')
    # if not args.StatusOff:
    #     print "============Run iSAFE============"
    #     print "Sliding window size: %i SNPs"%w_size
    #     print "Step size: %i SNPs"%w_step
    #     print "Top k: %i"%top_k1
    #     print "Max Rank: %i"%top_k2
    #     #print "StatusOff: %s" % args.StatusOff
    #     print "================================"
if __name__ == '__main__':
    run()