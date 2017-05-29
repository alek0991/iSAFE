iSAFE: **i**ntegrated **S**election of **A**llele **F**avored by **E**volution
==========
Methods that scan population genomics data to identify signatures of selective sweep have
been actively developed, but mostly do not identify the specific mutation favored by the selective
sweep. We present a method, iSAFE that uses population genetics signals and a boosting
approach to pinpoint the favored mutation even when the signature of selection extends to 5Mbp.

Input:
==========
Consider a sample of phased haplotypes in a genomic region. We assume that all 
sites are biallelic and  polymorphic in the sample. 
Thus, our input is in the form of a binary 
SNP matrix with each column corresponding to a haplotype and each row to a 
mutation, and entries corresponding to the allelic state, with 0 denoting the
ancestral allele, and 1 denoting the derived allele. iSAFE can take input in [hap](https://github.com/alek0991/iSAFE/blob/master/hap_format.md) or [vcf](https://samtools.github.io/hts-specs/VCFv4.2.pdf) formats. Note that in vcf mode, iSAFE accepts VCF and indexed bgzipped VCF (.vcf.gz plus .vcf.gz.tbi) with the file type detected
automatically.

Output:
==========
The output is a non-negative iSAFE-score for each mutation, according to its 
likelihood of being the favored variant of the selective sweep.

Requirements
==========
1. ```Python2.7```. Following python packages are required:
    - ```numpy``` version 1.9 or above.
    - ```pandas``` version 0.18.0 or above.
2. ```bcftools``` version 1.2 or above.
    - Please follow the [bcftools installation guideline](http://www.htslib.org/download/).
    - iSAFE assumes the bcftools binary file is installed to a bin subdirectory that is added to your $PATH. Otherwise, you have to change the following line in ```./src/bcftools.py``` to the bcftools binary file path: 
```sh
bcftools = "bcftools"
```

EXECUTION:
===========
Use the following command to see all the available options in iSAFE.
 
```sh
python2.7 ./src/isafe.py --help
```
This information is also provided in [./help.txt](https://github.com/alek0991/iSAFE/blob/master/help.txt).

Demo 1: input in [hap](https://github.com/alek0991/iSAFE/blob/master/hap_format.md) format
===========
With ```--format hap```, iSAFE assumes that derived allele is 1 and ancestral allele is 0 in the input file, and the selection is ongoing (the favored mutation is not fixed).
```sh
python2.7 ./src/isafe.py --input ./example/hap/demo.hap --output ./example/hap/demo --format hap
```
* 5Mbp region simulated by [msms](http://www.mabs.at/ewing/msms/index.shtml).
* Position of the favored mutation is 2,500,000.
 
Demo 2: input in [vcf](https://samtools.github.io/hts-specs/VCFv4.2.pdf) format
===========
Data Requirements:
*  Download Homo-Sapiens ```Ancestral Allele``` files:
    - Download links: 
        - [GRCh37/hg19](http://ftp.ensembl.org/pub/release-75/fasta/ancestral_alleles/)
        - [GRCh38/hg38](http://ftp.ensemblorg.ebi.ac.uk/pub/release-88/fasta/ancestral_alleles/)
    - unzip the files.
* Download 1000 Genome Project phased ```vcf``` files:
    - Download links: 
        - [GRCh37/hg19](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/)
        - [GRCh38/hg38](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/)
    - Better to use compressed vcf files ```.vcf.gz``` for faster pre-processing.
    - In case you are using ```.vcf.gz``` the index file ```.vcf.gz.tbi``` is also required by bcftools.

Run:
```sh
python2.7 ./src/isafe.py --input <chr2 vcf file> --output ./example/vcf/LCT --region 2:134108646-139108646 --AA <chr2 Ancestral Allele file> --vcf-cont <chr2 vcf file> --sample-case ./example/vcf/case.sample --sample-cont ./example/vcf/cont.sample
```
* 5Mbp region around LCT/MCM6 gene in FIN population. 
* Position of the [putative favored mutation](http://www.nature.com/ng/journal/v30/n2/full/ng826.html) is 136,608,646 (GRCh37/hg19).

