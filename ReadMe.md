iSAFE: **i**ntegrated **S**election of **A**llele **F**avored by **E**volution
==========
[![release](https://img.shields.io/github/v/release/alek0991/iSAFE)](ChangeLog.md)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/isafe/badges/version.svg)](https://anaconda.org/bioconda/isafe)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/isafe/badges/downloads.svg)](https://anaconda.org/bioconda/isafe)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/isafe/badges/latest_release_date.svg)](https://anaconda.org/bioconda/isafe)

Most approaches that capture signatures of selective sweeps in population genomics data do not identify the specific mutation favored by selection. The iSAFE enables researchers to accurately pinpoint the favored mutation in a large region (∼5 Mbp) by using a statistic derived solely from population genetics signals. iSAFE does not require knowledge of demography, the phenotype under selection, or functional annotations of mutations. 
- Akbari, Ali, Joseph J. Vitti, Arya Iranmehr, Mehrdad Bakhtiari, Pardis C. Sabeti, Siavash Mirarab, and Vineet Bafna. "Identifying the favored mutation in a positive selective sweep." [Nature Methods (2018)](https://doi.org/10.1038/nmeth.4606).
- Contact: Ali Akbari (Ali_Akbari@hms.harvard.edu). If I can be of assistance, please do not hesitate to contact me.


FAQ – frequently asked questions
==========
Please read the [FAQ](https://github.com/alek0991/iSAFE/blob/master/FAQ.md) for answers to the most common queries.

Conda Installation
==========
**On 64-bit Linux and Mac OSX**, you can install iSAFE from [bioconda channel](https://bioconda.github.io/user/install.html) using conda package manager. iSAFE v1.1.0 and later is compatible with both python 2 and python 3.
1. Install [Miniconda](https://bioconda.github.io/user/install.html) (you can skip this if you already have either of Miniconda or Anaconda installed). 
2. Add the bioconda channel by running the following commands in your terminal (order matters):
```sh
    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge
```
3. Run the following command to install iSAFE (and all dependencies) 
```sh
    conda install isafe
```

Manual installation: Software requirements
==========   

**Alternatively, and for all other OS and architectures**, you can download the github repository and install isafe using the setup script. 

1. Following python packages are required:
    -   ```numpy``` version 1.9 or above 
    -   ```pandas``` version 0.18 or above
2. Install ```bcftools``` version 1.2 or above (only for ```--format vcf```, not required if you are using ```--format hap```).
    - Follow the [bcftools installation guideline](http://www.htslib.org/download/).
    - iSAFE assumes the bcftools binary file is installed to a bin subdirectory that is added 
     to your ```$PATH```; otherwise, you have to change the following 
     [line](https://github.com/alek0991/iSAFE/blob/cc8d6f3c9fcdfe0625ed5aff93c0e940d9418e45/isafe/bcftools.py#L11) in ```./isafe/bcftools.py``` to the bcftools binary file path: 
    ```python
    bcf_tools = "bcftools"
    ``` 

3. Clone the github repository by running (or you can download the repo)
```sh
    git clone https://github.com/alek0991/iSAFE.git
```
4. Change to the iSAFE directory and run
```sh
    python setup.py install
```

Execution:
===========

Use the following command to see all the available options in iSAFE.
 
```sh
isafe --help
```
These detailed instructions are also provided in [./help.txt](https://github.com/alek0991/iSAFE/blob/master/help.txt).

**Note:** If you have a script for iSAFE<v1.1.0 and want to update to the latest version you should change the commands from 
```sh
python ./src/isafe.py [Options]
```
to
```sh
isafe [Options]
```

Input:
==========
Consider a sample of phased haplotypes in a genomic region. We assume that all 
sites are biallelic and  polymorphic in the sample. 
Thus, our input is in the form of a binary 
SNP matrix with each column corresponding to a haplotype and each row to a 
mutation, and entries corresponding to the allelic state, with 0 denoting the
ancestral allele, and 1 denoting the derived allele. Not surprisingly, iSAFE performance deteriorated when the favored mutation is fixed or near fixation (favored allele frequency (ν) > 0.9 in [Supplementary Fig. 3e](https://www.nature.com/articles/nmeth.4606/figures/6)). To handle this special case, we included individuals from non-target populations, using a specific protocol (See online [Methods](https://www.nature.com/articles/nmeth.4606#methods), section *Adding outgroup samples*). iSAFE can take input in [hap](https://github.com/alek0991/iSAFE/blob/master/hap_format.md) or [vcf](https://samtools.github.io/hts-specs/VCFv4.2.pdf) formats.
* [hap](https://github.com/alek0991/iSAFE/blob/master/hap_format.md) format: ```--format hap``` or ```-f hap```. With hap format, iSAFE assumes:
    - Derived allele is 1 and ancestral allele is 0 in the input file.
    - The selection is ongoing (the favored mutation is not fixed). In the current implementation of iSAFE with ```--format hap```, user is required to add outgroup samples to the input hap file if needed, based on this simple protocol mentioned above.
    - Consequently, input with hap format is not allowed with any of these: ```--vcf-cont```, ```--sample-case```, ```--sample-cont```, ```--AA```.
* [vcf](https://samtools.github.io/hts-specs/VCFv4.2.pdf) format (Default): ```--format vcf``` or ```-f vcf```
    - Only phased vcf files are accepted.
    - In v1.0.1 or above it keeps not SNPs (indels, MNPs, and etc) as long as they have only one ALT (binary alleles).
    - vcf format only accepts indexed bgzipped VCF (vcf.gz with index file) or indexed bcf files (.bcf with index file).
    - The Ancestral Allele file (```--AA```) must be provided with ```--format vcf```. From version 1.0.5, if the ancestral allele file (--AA) is not available the program raises a warning and assumes reference allele (REF) is ancestral allele.
    - You can choose a subset of samples in the input vcf file by using ```--sample-case```. Otherwise all the samples in the input vcf file are considered as the case samples. See [sample ID file format](https://github.com/alek0991/iSAFE/blob/master/sample_ID_format.md).
    - ```--vcf-cont``` is optional but recommended for capturing fixed sweeps. You can choose a subset of samples in this file by using ```--sample-cont``` option, otherwise all the samples in this file are cosidered as control population. See [sample ID file format](https://github.com/alek0991/iSAFE/blob/master/sample_ID_format.md).  
    - You must use ```--sample-case``` and ```--sample-cont``` when the ```--input``` and ```--vcf-cont``` are the same (all samples are provided in a single vcf file).

**Note:** The software in vcf mode is more flexible and has more options. But if you don't have out-group samples (```--vcf-cont``` is not set), and hap file and vcf file contain the _exact_ same information (iSAFE only cares about position, haplotype phase, derived allele (1), and ancestral allele (0) in the vcf mode), then the output of iSAFE must be identical.

Output:
==========
The output is a non-negative iSAFE-score for each mutation, according to its 
likelihood of being the favored variant of the selective sweep. 
Result (```<output>.iSAFE.out```) is a TAB separated file in the following format.

| POS | iSAFE | DAF |
|:----------:|:---------:|:---------:|
| 291 |    0.02    |    0.05    |
| 626 |    0.01    |    0.55    |
| ... |    ...    |    ...    |

With following headers:

   - POS: Position (bp) sorted in ascending order
   - iSAFE: Non-negative iSAFE score
   - DAF: Derived allele frequency

Data availability for vcf format
==========
*  Download Homo-Sapiens Ancestral Allele files in case you are using ```--format vcf``` and consequently ```--AA```:
    - Download links: 
        - [GRCh37/hg19](http://ftp.ensembl.org/pub/release-75/fasta/ancestral_alleles/)
        - [GRCh38/hg38](http://ftp.ensemblorg.ebi.ac.uk/pub/release-88/fasta/ancestral_alleles/)
    - You need to unzip the files.
* The 1000 Genome Project phased vcf files can be used as ```--input``` or ```--vcf-cont```:
    - Download links: 
        - [GRCh37/hg19](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/)
        - [GRCh38/hg38](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/)
    - You can use your own data and you don't have to use 1000GP data as ```--input``` (case) or ```--vcf-cont``` (control).
    - Only accepts indexed bgzipped VCF (vcf.gz with index file) or indexed bcf files (.bcf with index file) for faster pre-processing
    - The index file is also required by bcftools.


Demo 1: input in [hap](https://github.com/alek0991/iSAFE/blob/master/hap_format.md) format
===========
With ```--format hap```, iSAFE assumes that derived allele is 1 and ancestral allele is 0 in the input file, and the selection is ongoing (the favored mutation is not fixed).
```sh
isafe --input ./example/hap/demo.hap --output ./example/hap/demo --format hap
```
* 5Mbp region simulated by [msms](http://www.mabs.at/ewing/msms/index.shtml).
* Position of the favored mutation is 2,500,000.

Demo 2: input in [vcf](https://samtools.github.io/hts-specs/VCFv4.2.pdf) format
===========
Follow the instructions in the [Data Requirements section](https://github.com/alek0991/iSAFE#data-requirements) and download Homo-Sapiens Ancestral Allele files and phased vcf files of Chromosome 2 of 1000GP populations (GRCh37/hg19), and replace the text in each ```< >``` with the proper file path.


<h4>Scenario 1: All samples</h4> 

All the samples of the ```--input``` vcf file as the case population:
- The following command apply iSAFE on 5Mbp region around LCT/MCM6 locus in all 2504 samples (5008 haplotypes) of 1000GP as the case population.
    
```sh
isafe --input <chr2 vcf file> --output ./example/vcf/LCT --region 2:134108646-139108646 --AA <chr2 Ancestral Allele file>
```

<h4>Scenario 2: A subset of samples</h4>
 
A subset of samples (```--sample-case```) of the ```--input``` vcf file as the case population:
- The following command apply iSAFE on 5Mbp region around LCT/MCM6 locus in FIN population of 1000GP as the case population.

```sh
isafe --input <chr2 vcf file> --output ./example/vcf/LCT --region 2:134108646-139108646 --AA <chr2 Ancestral Allele file> --sample-case ./example/vcf/case.sample
```

<h4>Scenario 3: Adding outgroup samples</h4>
 
 A subset of samples (```--sample-case```) of the ```--input``` vcf file as the case population and a subset of samples (```--sample-cont```) of the ```--vcf-cont``` vcf file as the control population:
- The following command apply iSAFE on 5Mbp region around LCT/MCM6 locus in FIN population of 1000GP as the case population and YRI, CHB, PEL, and GIH as the control populations.

```sh
isafe --input <chr2 vcf file> --output ./example/vcf/LCT --region 2:134108646-139108646 --AA <chr2 Ancestral Allele file> --vcf-cont <chr2 vcf file> --sample-case ./example/vcf/case.sample --sample-cont ./example/vcf/cont.sample
```

* ```--input``` and ```--vcf-cont``` can point to the same vcf file or different ones. In case they are the same, ```--sampe-case``` and ```--sample-cont``` are mandatory.
* Position of the [putative favored mutation in the FIN population](http://www.nature.com/ng/journal/v30/n2/full/ng826.html) for the selective sweep around LCT/MCM6 locus is 136,608,646 (GRCh37/hg19) of chromosome 2.
