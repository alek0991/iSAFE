In progress ...
==========

iSAFE: **i**ntegrated **S**election of **A**llele **F**avored by **E**volution
==========

Requirements
==========
1. ```Python2.7```. Following python packages are required:
    - ```numpy``` version 1.9 or above
    - ```pandas``` version 0.18.0 or above
2. ```bcftools``` version 1.3.1
    - Please follow the [bcftools installation guideline](http://www.htslib.org/download/).
    - iSAFE assumes the bcftools binary file is installed to a bin subdirectory that is added to your $PATH. Otherwise, you have to change the following line in ```./src/bcftools.py``` to the bcftools binary file path: 
```sh
bcftools = "bcftools"
```


Demo: [hap format](https://github.com/alek0991/iSAFE/blob/master/example/hap/ReadMe.md)
===========
```sh
$ python2.7 ./src/isafe.py --input ./example/hap/demo.hap --output ./example/hap/demo --format hap
```
* 5Mbp region simulated by [msms](http://www.mabs.at/ewing/msms/index.shtml)
* Favored mutation Position is 2,500,000
 
Demo: [vcf format](https://samtools.github.io/hts-specs/VCFv4.2.pdf)
===========
Data Requirements
*  Download Homo-Sapiens ```Ancestral Allele``` files:
    - [GRCh37/hg19](http://ftp.ensembl.org/pub/release-75/fasta/ancestral_alleles/)
    - unzip the files 
* Download 1000 Genome Project phased ```vcf``` files:
    - [GRCh37/hg19](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/)
    - Better to use compressed vcf files ```.vcf.gz``` for faster pre-processing   
    - In case you are using ```.vcf.gz``` the index file ```.vcf.gz.tbi``` is also required by bcftools.
```sh
$ python2.7 ./src/isafe.py --input <chr2 vcf file> --output ./example/vcf/LCT --region 2:134108646-139108646 --AA <chr2 Ancestral Allele file> --vcf-cont <chr2 vcf file> --sample-case ./example/vcf/case.sample --sample-cont ./example/vcf/cont.sample
```
* 5Mbp region simulated by [msms](http://www.mabs.at/ewing/msms/index.shtml)
* Favored mutation Position is 2,500,000

