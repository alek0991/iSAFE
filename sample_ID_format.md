Sample ID file format
==========
```--sample-case```/```--sample-cont``` requires a text file with two columns. The first one is population and the second column
                            is sample ID's. Samples must be a subset of ID's used in the ```--input```/```--vcf-cont``` vcf file, respectively.
                            
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
