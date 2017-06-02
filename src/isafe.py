import argparse
import warnings
import pandas as pd
from isafeclass import iSafeClass
from safeclass import SafeClass
from utils import *
from bcftools import get_snp_matrix
def run():
    # command line parser
    parser = argparse.ArgumentParser(description='===================================================================='
                                                 '\niSAFE: (i)ntegrated (S)election of (A)llele (F)avored by (E)volution'
                                                 '\n===================================================================='
                                                 '\nSource code & further instructions can be found at: https://github.com/alek0991/iSAFE'
                                                 '\niSAFE v1.0.0'
                                                 '\n--------------------------------------------------------------------', formatter_class=argparse.RawTextHelpFormatter)

    # optional arguments
    parser.add_argument('--format', '-f',help='<string>: Input format. <FORMAT> must be either hap or vcf (see the manual for more details).'
                                              '\niSAFE can handle two types of inputs (phased haplotypes are required):'
                                              '\n  * vcf format: --format vcf or -f vcf'
                                              '\n    - vcf format can handle both vcf.gz (.tbi file is required for bcftools) and vcf.'
                                              '\n    - When input format is vcf, Ancestral Allele file (--AA) must be given.'
                                              '\n  * hap format: --format hap or -f hap'
                                              '\n    - Input with hap format is not allowed with any of these: --vcf-cont, --sample-case, --sample-cont, --AA.'
                                              '\n    - With hap format, iSAFE assumes that derived allele is 1 and ancestral allele is 0 in the input file,\n      and the selection is ongoing (the favored mutation is not fixed).'
                                              '\nDefault: vcf', required=False, default='vcf')
    parser.add_argument('--input', '-i',help='<string>: Path to the input (case population).'
                                             '\n  * Input positions must be sorted numerically, in increasing order.', required=True)
    parser.add_argument('--output', '-o',help='<string>: Path to the output(s).'
                                              '\n  * iSAFE generates <OUTPUT>.iSAFE.out'
                                              '\n  * When --OutputPsi is set, iSAFE generates <OUTPUT>.Psi.out in addition to <OUTPUT>.iSAFE.out'
                        , required=True)

    parser.add_argument('--vcf-cont', help='<string>: Path to the phased control population in .vcf or .vcf.gz format.'
                                           '\n  * This is optional but recommended for capturing fixed sweeps.'
                                           '\n  * This option is only available with --format vcf.'
                                           '\n  * You can choose a subset of samples in this file by using --sample-cont option,\n    otherwise all the samples in this file are cosidered as control population.'
                                           '\n  * You must use --sample-case and --sample-cont when --input and --vcf-cont are the same (all samples are provided in a single vcf file).'
                                           '\n  * You can (you don\'t have to) use 1000 Genome Project populations as control.'
                                           '\n    - Download link of phased VCF files of 1000GP (GRCh37/hg19): http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/'
                                           '\n    - Download link of phased VCF files of 1000GP (GRCh38/hg38): http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/'
                                           '', required=False)
    parser.add_argument('--sample-case', help='<string>: Path to the file containing sample ID\'s of the case population.'
                                              '\n  * This option is only available in --format vcf.'
                                              '\n  * When this option is not used all the samples in the --input are considered as the case samples.'
                                              '\n  * This file must have two columns, the first one is population and the second column\n    is sample ID\'s (must be a subset of ID\'s used in the --input vcf file).'
                                              '\n  * This file must be TAB separated, no header, and comments by #.'
                                              '\n  * You must use --sample-case and --sample-cont when --input and --vcf-cont are the same (all samples are provided in a single vcf file).'
                                              '\n  * Population column (first column) can have more than one population name. They are all considered the case populations.'
                                              '\n  * Sample ID\'s must be subset of the --input vcf file', required=False)
    parser.add_argument('--sample-cont', help='<string>: Path to the file containing sample ID\'s of the control population(s).'
                                              '\n  * This option is only available in --format vcf.'
                                              '\n  * When this option is not used all the samples in the --vcf-cont are considered as the control samples.'
                                              '\n  * This file must have two columns, the first one is population and the second column\n    is sample ID\'s (must be a subset of ID\'s used in the --vcf-cont file).'
                                              '\n  * This file must be TAB separated, no header, and comments by #.'
                                              '\n  * You must use --sample-case and --sample-cont when --input and --vcf-cont are the same (all samples are provided in a single vcf file).'
                                              '\n  * Population column (first column) can have more than one population name. They are all considered the control populations.'
                                              '\n  * Sample ID\'s must be subset of the --vcf-cont file', required=False)
    parser.add_argument('--AA', help='<string>: Path to the Ancestral Allele (AA) file in FASTA (.fa) format.'
                                     '\n  * This is required in --format vcf.'
                                     '\n  * Download link (GRCh37/hg19): http://ftp.ensembl.org/pub/release-75/fasta/ancestral_alleles/'
                                     '\n  * Download link (GRCh38/hg38): http://ftp.ensemblorg.ebi.ac.uk/pub/release-88/fasta/ancestral_alleles/'
                                     , required=False)
    parser.add_argument('--region', help='<chr:string>:<start position:int>-<end position:int>, the coordinates of the target region in the genome.'
                                         '\n  * This is required in --format vcf but optional in the --format hap.'
                                         '\n  * In vcf format, <chr> style (e.g. chr2 or 2) must be consistent with vcf files.'
                                         '\n  * The <chr> is dumped in --format hap.'
                                         '\n  * Valid Examples:'
                                         '\n      2:10000000-15000000'
                                         '\n      chr2:10000000-15000000'
                                         '\n      2:10,000,000-15,000,000'
                                         '\n      chr2:10,000,000-15,000,000'
                        , required=False)
    parser.add_argument('--MaxRegionSize', type=int, help='<int>: Maximum region size in bp.'
                                                          '\n  * Consider the memory (RAM) size when change this parameter.'
                                                          '\nDefault: 6000000', required=False, default=6000000)
    parser.add_argument('--MinRegionSize-bp', type=int, help='<int>: Minimum region size in bp.'
                                                          '\nDefault: 200000', required=False, default=200000)
    parser.add_argument('--MinRegionSize-ps', type=int, help='<int>: Minimum region size in polymorphic sites.'
                                                          '\nDefault: 1000', required=False, default=1000)
    parser.add_argument('--MaxGapSize', type=int, help='<int>: Maximum gap size in bp.'
                                                       '\n  * When there is a gap larger than --MaxGapSize the program raise an error.'
                                                       '\n  * You can ignore this by setting the --IgnoreGaps flag.'
                                                       '\nDefault: 10000', required=False, default=10e3)
    parser.add_argument('--window', type=int, help='<int>: Sliding window size in polymorphic sites.\nDefault: 300', required=False, default=300)
    parser.add_argument('--step', type=int, help='<int>: Step size of sliding window in polymorphic sites.\nDefault: 150', required=False, default=150)
    parser.add_argument('--topk', type=int, help='<int>: Rank of SNPs used for learning window weights (alpha).\nDefault: 1', required=False, default=1)
    parser.add_argument('--MaxRank', type=int, help='<int>: Ignore SNPs with rank higher than MAXRANK.'
                                                    '\n  * For considering all SNPs set --MaxRank > --window.'
                                                    '\n  * The higher the --MaxRank, the higher the computation time.'
                                                    '\nDefault: 15', required=False, default=15)
    parser.add_argument('--MaxFreq', type=float, help='<float>: Ignore SNPs with frequency higher than MaxFreq.\nDefault: 0.95',
                        required=False, default=0.95)
    parser.add_argument('--RandomSampleRate', type=float, help='<float>: Portion of added random samples.'
                                                               '\n  * RandomSampleRate = RandomSamples/(RandomSamples+CaseSamples).'
                                                               '\n  * Must be non-negative and less than 1.\nDefault: 0.1'
                                                               '\n  * Ignored when --vcf-case is not used.'
                                                               '\n  * Ignored when MDDAF criterion doesn\'t recommend adding random samples. The option --ForceRandomSample'
                                                               '\n    can be used to override MDDAF criterion.'
                        , required=False, default=0.1)
    parser.add_argument('--ForceRandomSample', '-FRS', help='<bool>: Set this flag to force the iSAFE to use random samples even when MDDAF doesn\'t recommend.'
                                                            '\n  * --vcf-cont must be provided.'
                                                            '\nDefault: false', action='store_true')
    parser.add_argument('--IgnoreGaps', '-IG', help='<bool>: Set this flag to ignore gaps.\nDefault: false', action='store_true')
    parser.add_argument('--StatusOff', '-SO', help='<bool>: Set this flag to turn off printing status.\nDefault: false', action='store_true')
    parser.add_argument('--WarningOff', '-WO', help='<bool>: Set this flag to turn off warnings.\nDefault: false',
                        action='store_true')
    parser.add_argument('--OutputPsi', '-Psi', help='<bool>: Set this flag to output Psi_1 in a text file with suffix .Psi.out.'
                                                    '\nDefault: false', action='store_true')
    parser.add_argument('--SAFE', help='<bool>: Set this flag to report the SAFE score of the entire region.'
                                       '\n  * When the region size is less than --MinRegionSize-ps (Default: 1000 SNPs) or --MinRegionSize-bp (Default: 200kbp), '
                                       '\n    the region is too small for iSAFE analysis. Therefore, It\'s better to use --SAFE flag to report the SAFE scores of '
                                       '\n    the entire region instead of iSAFE scores.'
                                                    '\nDefault: false', action='store_true')
    args = parser.parse_args()

    if (args.format not in ['hap', 'vcf']):
        raise ValueError("--format must be either hap or vcf.")
    if (args.format == 'hap'):
        if ((args.vcf_cont is not None)|(args.sample_case is not None)|(args.sample_cont is not None)|(args.AA is not None)):
            parser.error("[--format hap] is not allowed with any of these: --vcf-cont, --sample-case, --sample-cont, --AA.")
        else:
            if not args.WarningOff:
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
            if not args.WarningOff:
                warnings.warn("Warning: There is %i gaps with size greater than %ikbp." % (num_gaps, args.MaxGapSize/ 1e3))
    f = snp_matrix.mean(1)
    snp_matrix = snp_matrix.loc[((1 - f) * f) > 0]
    NumSNPs = snp_matrix.shape[0]
    if status:
        print "%i SNPs and %i Haplotypes" % (snp_matrix.shape[0], snp_matrix.shape[1])

    if args.SAFE:
        if not args.WarningOff:
            warnings.warn("The --SAFE flag is set. Therefore, output is the SAFE scores of the entire region (not the iSAFE scores).")
        obj_safe = SafeClass(snp_matrix.values.T)
        df_final = obj_safe.creat_dataframe().rename(columns={'safe':'SAFE', "freq":"DAF"})
        df_final['POS'] = snp_matrix.index
        df_final[["POS", "SAFE", "DAF", "phi", "kappa"]].to_csv("%s.SAFE.out"%args.output, index=None,sep='\t')
        if status:
            print "SAFE Done!"
    else:
        if (NumSNPs < args.MinRegionSize_bp) | (total_window_size < args.MinRegionSize_ps):
            raise ValueError((
                             "The region Size is %i SNPs and %ikbp. When the region size is less than --MinRegionSize-ps (%i) SNPs or --MinRegionSize-bp (%ikbp), "
                             "the region is too small for iSAFE analysis and better to use --SAFE flag to report "
                             "the SAFE score of the entire region." % (
                             NumSNPs, total_window_size / 1e3, args.MinRegionSize_ps, args.MinRegionSize_bp / 1e3)))
        obj_isafe = iSafeClass(snp_matrix, args.window, args.step, args.topk, args.MaxRank)
        obj_isafe.fire(status=status)
        df_final = obj_isafe.isafe.loc[obj_isafe.isafe["freq"]<args.MaxFreq].sort_values("ordinal_pos").rename(columns={'id':"POS", 'isafe':'iSAFE', "freq":"DAF"})
        df_final[["POS", "iSAFE", "DAF"]].to_csv("%s.iSAFE.out"%args.output, index=None,sep='\t')
        if args.OutputPsi:
            psi_k1 = obj_isafe.creat_psi_k1_dataframe()
            psi_k1.index.rename("#POS", inplace=True)
            psi_k1.to_csv("%s.Psi.out"%args.output, sep='\t')
if __name__ == '__main__':
    run()