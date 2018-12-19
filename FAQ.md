
FAQ – frequently asked questions
=============
<h4>Questions: </h4> 

Do I have to add random samples?

>When the favored mutation is near fixation (or fixed) the performance of the iSAFE decays. Not surprisingly, adding random sample from outgroup populations improves the iSAFE performance when frequency of the favored mutation is high. Because iSAFE is comparing diversity of carriers and non-carriers of mutations  and without outgroup samples we don't have any (or enough) outgroup samples when the favored mutation is fixed (or at high frequency). Besides, not using outgroup samples (cross-population information) is a waste of (orthogonal) information, specifically for human populations with all these valuable resources like 1000GP. 
>However, when frequency of the favored mutation is not high (low or moderate), adding random samples doesn't help. For more details see [Supplementary Figure 3e](https://www.nature.com/articles/nmeth.4606/figures/6) and Section *Adding outgroup samples* from [online methods](https://www.nature.com/articles/nmeth.4606#methods).
>
>Given proper outgroup populations (using ```--vcf-cont```and ```--sample-cont``` arguments) the program calculates Eq. 6 ([online methods](https://www.nature.com/articles/nmeth.4606#methods)) and automatically decides whether random samples are required or not. As an example see the [**Scenario 3 of the Demo 2**](https://github.com/alek0991/iSAFE#demo-2-input-in-vcf-format).

<h4>Questions: </h4>

Which outgroup populations should we use?

>In the Section *Adding outgroup samples* from [online methods](https://www.nature.com/articles/nmeth.4606#methods), we mentioned that "*in testing on the phase 3 1000GP data, we chose outgroup samples from non-target 1000GP populations.*" For example for East-Asian sub-populations (like CHB+JPT) you can use AFR+AMR+EUR+SAS populations, or whatever combination of populations you prefer. Just make sure there are not any shared samples between the target population samples and outgroup samples, otherwise the program raises the following error:
```Error: --sample-case and/or --sample-cont have shared/duplicated samples.```  Also make sure to use the rigth format for the [sample ID file](https://github.com/alek0991/iSAFE/blob/master/sample_ID_format.md). 

<h4>Questions: </h4>

Can we change the default values of ```RandomSampleRate``` or ```MaxFreq``` parameters?

>The default values for ```RandomSampleRate=0.10``` and for ```MaxFreq=0.95```, and it is fine to change them. As a rule of thumb, I usually set ```MaxFreq = 1-(RandomSampleRate/2)``` , to minimize the noise due to adding outgroups.

<h4>Questions: </h4>

Should we change the default value of ```MaxRank``` parameter?

>The ```MaxRank``` parameter is defined to control the computation time and it increases linearly with this parameter. The program doesn't calculate iSAFE score for a SNP that its SAFE-score is not in the top-15 (top-MaxRank) in windows overlapping the SNP. The default value of sliding window size is ```window=300``` segregating sites. 
>
>In most of the cases (&gt;99%, See [Figure 1e](https://www.nature.com/articles/nmeth.4606/figures/1)), the default value for ```MaxRank=15``` works just fine and the favored mutation is included and its iSAFE score is calculated and reported in the output file. In some rare cases you might not capture the favored mutation with the default value (```MaxRank=15```). Therefore you can make sure that you are not missing the favored mutation 100%, by setting ```MaxRank=300```, or whatever value &#8805; ``` window``` (default: 300).

<h4>Questions: </h4>

When I try to run my vcf files the result is ```Error: There are <i> gaps with size greater than 10kbp.```
 
>When there is a gap larger than ```MaxGapSize``` (default: 10kbp) the program raise an error. You can ignore this by setting the ```--IgnoreGaps``` flag or you can change the maximum gap size threshold by ```--MaxGapSize```.


<h4>Questions: </h4>

Does iSAFE program handle haploid samples?

>Yes, when ploidy is consistent for all samples over all sites the program automatically handles ploidy.
 If one sample have more than a ploidy in different region of your file it is inconsistent. 
You can use the [```bcftools plugin check-ploidy```](http://samtools.github.io/bcftools/howtos/plugins.html) 
to check ploidy of your target region. For example, in the first column ("[1]Sample") of the output of the following 
command all the values must be unique, otherwise ploidy is inconsistent for repeated samples.
>
> ```bcftools plugin check-ploidy -r X:2000000-5000000 chrX.vcf.gz```

<h4>Questions: </h4>

When should I use the ```--SAFE``` flag?
> In [Figure 2c](https://www.nature.com/articles/nmeth.4606/figures/2) we have evaluated the performance of SAFE and iSAFE as a function of the window size. 
iSAFE exploits shoulders of the sweep using the SAFE score as a building block and it performance stays robust with increasing window size. 
In contrast, SAFE is not exploiting the shoulders. It is effective when the region size is small (few recombinations). 
As a rule of thumb, if you region is small (&lt;200kbp or &lt;1000 segregating sites) use SAFE.

<h4>Questions: </h4>

How to pick a size for the target region?

>If the signal is very strong, Like LCT locus in European populations, 5Mbp is more than enough for iSAFE to exploit information from 
the shoulders and identify the favored mutation. For weaker signals you can go with smaller window like 1Mbp or even 500kbp. 
It depend on what are you exactly doing. For example, 
>* If you are scanning the whole genome, based on my experience for human data, I would recommend a 3 Mbp window with 1Mbp step-size.  
>* If you are focused on specific region, like LCT, You can play with different window sizes to get a sense of the region. The rank of the favored mutation and shape of the signal usually don't change when you change the window size.  It really doesn't matter as long as you fix the window size and calculate the P value based on that window size. In our paper we picked 5Mbp but we could use larger or smaller window size. Therefore, if you want to use iSAFE, pick a large window (like 500kbp, 1Mbp,  2Mbp, 3Mbp, and so forth) and fix that and start your analysis.
>* If you are confident that the favored mutation is within a small window (~100kbp) you can apply SAFE. Always keep in mind that you might get stuck in the [shoulder](https://doi.org/10.1534/genetics.115.174912) of another sweep and think your region is under selection. This is one of the reasons we devised iSAFE.