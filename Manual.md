iSAFE can handle to types of inputs (The default format is vcf):
* vcf format: ```--format vcf``` or ```-f vcf```
    - vcf format can handle both vcf.gz (.tbi file is required for bcftools) and vcf.
    - When input format is vcf, [Ancestral Allele file](http://ftp.ensembl.org/pub/release-75/fasta/ancestral_alleles/) (```--AA```) must be given.
* hap format: ```--format hap``` or ```-f hap```
    - Input with hap format is not allowed with any of these: ```--vcf-cont```, ```--sample-case```, ```--sample-cont```, ```--AA```.
    - With hap format, iSAFE assumes that derived allele is 1 and ancestral allele is 0 in the input file, and the selection is ongoing (the favored mutation is not fixed).
