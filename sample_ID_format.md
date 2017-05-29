hap format
==========
```--sample-case```/```--sample-cont``` requires a text file with two columns. The first one is population and the second column
                            is sample ID's (must be a subset of ID's used in the ```--input```/```--vcf-cont``` vcf file).
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

