iSAFE Frequently asked questions (FAQ)
==========
Question: When I try to run my vcf files the result is "ValueError: There is 1 gaps with size greater than 10kbp."
   - Answer: When there is a gap larger than ```--MaxGapSize``` (default: 10kbp) the program raise an error. You can ignore this by setting the ```--IgnoreGaps``` flag or you can change the maximume gap size threshold by ```--MaxGapSize```.    