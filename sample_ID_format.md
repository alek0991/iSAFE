hap format
==========
```--sample-case```/```--sample-cont``` requires a text file with two columns. The first one is population and the second column
                            is sample ID's (must be a subset of ID's used in the ```--input```/```--vcf-cont``` vcf file).
                            
Example
==========
| #Population | Sample|
|:----------:|:---------:|
|FIN|HG00171|
|FIN|HG00173|
|...|...|
|YRI|NA19144|
|YRI|NA19146|
|...|...|


Notes
==========
* TAB separated  
* No Header  
* Comment by #
* Positions must be sorted numerically, in increasing order

