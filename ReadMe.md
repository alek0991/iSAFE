In progress ...
==========

iSAFE: **i**ntegrated **S**election of **A**llele **F**avored by **E**volution
==========

Requirements
==========
1. ```Python2.7```. Following python packages are required:
- ```numpy``` version 1.9 or above
- ```pandas``` version 0.18.0 or above
2. ```bcftools``` version 1.4.1
- Please follow the [bcftools installation guideline](http://www.htslib.org/download/).
- iSAFE assumes the bcftools binary file is installed to a bin subdirectory that is added to your $PATH. Otherwise, you have to change the following line in ```./src/bcftools.py``` to the bcftools binary file path: 
```sh
bcftools = "bcftools"
```


 
Demo
===========
```sh
$ python2.7 ./src/isafe.py --input ./example/hap/demo.hap --output ./example/hap/demo --format hap
```
* 5Mbp simulated region
* Favored mutation Position is 2,500,000