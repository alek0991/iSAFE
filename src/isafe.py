#!/usr/bin/python

import argparse
import pandas as pd
from isafeclass import iSafeClass
from utils import drop_duplicates

def run():
    # command line parser
    parser = argparse.ArgumentParser(description='iSAFE: (i)ntegrated (S)election of (A)llele (F)avored by (E)volution')

    # input
    parser.add_argument('input_path', help='Path to the input file')
    parser.add_argument('output_path', help='Path to the output file(s), proper suffix will be added automatically, e.g. *.isafe.out, *.psi_k1.out')

    # optional arguments
    parser.add_argument('--wsize', type=int, help='Sliding window size (variant count) [300]', required=False, default=300)
    parser.add_argument('--step', type=int, help='Step size (variant count) for sliding window [150]', required=False, default=150)
    parser.add_argument('--topk', '-k', type=int, help='Rank of SNPs used for learning windows weights (alpha) [1]', required=False, default=1)
    parser.add_argument('--MaxRank', '-MR', type=int, help='Ignore SNPs with rank higher than MAXRANK [10]', required=False, default=15)
    parser.add_argument('--MaxFreq', '-MF', type=float, help='Ignore SNPs with frequency higher than MAXFreq [0.95]',
                        required=False, default=0.95)
    parser.add_argument('--StatusOff', '-SO', help='Set if you want to print status', action='store_true')
    parser.add_argument('--DropDuplicates', '-DD', help="Set if you want to drop all instances of duplicated SNP ID's.", action='store_true')
    parser.add_argument('--OutputPsi', '-Psi', help='Output Psi_k1 in a text file with .psi_k1.out', action='store_true')
    args = parser.parse_args()

    input_file = args.input_path
    output_file = args.output_path
    w_size = args.wsize
    w_step = args.step
    top_k1 = args.topk
    top_k2 = args.MaxRank
    DropDuplicates = args.DropDuplicates
    status = not args.StatusOff
    if status:

        print "============Run iSAFE============"
        print "input: %s"%input_file
        print "output: %s.isafe.out"%output_file
        print "Sliding window size: %i SNPs"%w_size
        print "Step size: %i SNPs"%w_step
        print "Top k: %i"%top_k1
        print "Max Rank: %i"%top_k2
        if DropDuplicates:
            print "DropDuplicates: %s"%DropDuplicates
        #print "StatusOff: %s" % args.StatusOff
        print "================================"
    snp_matrix = pd.read_csv(input_file, sep=",", header=None, comment='#')
    drop_duplicates(snp_matrix, DropDuplicates)
    snp_matrix.set_index(0, inplace=True)
    if status:
        print "%i SNPs and %i Haplotypes"%(snp_matrix.shape[0], snp_matrix.shape[1])
    obj_isafe = iSafeClass(snp_matrix, w_size, w_step, top_k1, top_k2)
    obj_isafe.fire(status=status)
    obj_isafe.isafe.loc[obj_isafe.isafe["freq"]<args.MaxFreq].sort_values("ordinal_pos").to_csv("%s.isafe.out"%output_file, index=None)
    if args.OutputPsi:
        psi_k1 = obj_isafe.creat_psi_k1_dataframe()
        psi_k1.to_csv("%s.psi_k1.out"%output_file)
if __name__ == '__main__':
    run()