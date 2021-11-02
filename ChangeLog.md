* Version 1.1.1
    - remove pysam as dependency
* Version 1.1.0
    - Made compatible with both python 2 and 3
    - Added Conda installation with all dependecies
    - Command changed from ```python ./src/isafe.py [Options]``` to ```isafe [Options]```
* Version 1.0.7
    - Fix bug for reading indexed BCF files
    - Raise error in create_rolling_indices() in isafeclass.py when total number of variants is smaller than --window
    - Raise error when  --window is smaller than --MinRegionSize-ps
    - Raise error when  --window is smaller than --step
    - Print version (-v, --version)
* Version 1.0.6
    - Fixed bug with numerical sample names.
* Version 1.0.5
    - If the ancestral allele file (--AA) is not available the program raises a warning and assumes reference allele (REF) is ancestral allele.
* Version 1.0.4
    - Raise error for inconsistent ploidy, non-biallelic, and empty region. 
* Version 1.0.3
    - Handling male (haploid) samples for chromosome X.
* Version 1.0.2
    - Track execution progress and fixing minor bugs.
* Version 1.0.1
    - Keeps not SNPs (indels, MNPs, and etc) as long as they have only one ALT (binary alleles).   