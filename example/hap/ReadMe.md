hap format
==========
A .hap file organizes variant data with rows representing a single haploid copy from an individual and
columns representing consecutive loci delimited by whitespace. For example,

==========
| Position(bp) | Haplotype 1A | Haplotype 1B | Haplotype 2A | Haplotype 2B | ... |
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
* Comment by #.  
