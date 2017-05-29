hap format
==========
A .hap file organizes SNP matrix of a population with phased haplotypes in a genomic region.
We assume that all sites are biallelic and polymorphic in the sample. Thus, our input is in
the form of a binary SNP matrix with each columns corresponding to a haplotype and each row
to a mutation, and entries corresponding to the allelic state, with 0 denoting the ancestral
allele, and 1 denoting the derived allele. The first column is corresponding to the position
of mutations.

Example
==========
| #Position(bp) | Haplotype 1A | Haplotype 1B | Haplotype 2A | Haplotype 2B | ... |
|:----------:|:---------:|:---------:|:---------:|:---------:|:--------------------:|
| 291 |    1    |    1    |    0    |    1    |    ...    |
| 626 |    0    |    0    |    0    |    1    |    ...    |
| 721 |    0    |    1    |    0    |    0    |    ...    |
| 1208 |    1    |    1    |    0    |    0    |    ...    |
| ... |    ...    |    ...    |    ...    |    ...    |    ...    |    ...    |

Notes
==========
* TAB separated  
* No Header  
* Comment by #
* Positions must be sorted numerically, in increasing order
