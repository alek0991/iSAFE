
FAQ – frequently asked questions
=============
<h4>Questions: </h4> 

Do I have to add random samples?

>When the favored mutation is near fixation (or fixed) the performance of the iSAFE decays. Not surprisingly, adding random sample from outgroup populations improves the iSAFE performance when frequency of the favored mutation is high. Because iSAFE is comparing diversity of carriers and non-carriers of mutations  and without outgroup samples we don't have any (or enough) outgroup samples when the favored mutation is fixed (or at high frequency). Besides, not using outgroup samples (cross-population information) is a waste of (orthogonal) information, specifically for human populations with all these valuable resources like 1000GP. 
>However, when frequency of the favored mutation is not high (low or moderate), adding random samples doesn't help. For more details see [Supplementary Figure 3e](https://www.nature.com/articles/nmeth.4606/figures/6) and [online methods](https://www.nature.com/articles/nmeth.4606#methods): Section *Adding outgroup samples*.
>
>Given proper outgroup populations (using ```--vcf-cont```and ```--sample-cont``` arguments) the program calculates Eq. 6 ([online methods](https://www.nature.com/articles/nmeth.4606#methods)) and automatically decides whether random samples are required or not. As an example see the [**Scenario 3 of the Demo 2**](https://github.com/alek0991/iSAFE#demo-2-input-in-vcf-format).

<h4>Questions: </h4>

Which outgroup populations should we use?

>In the [online methods](https://www.nature.com/articles/nmeth.4606#methods): Section *Adding outgroup samples* we mentioned that "*in testing on the phase 3 1000GP data, we chose outgroup samples from non-target 1000GP populations.*" For example for East-Asian sub-populations (like CHB+JPT) you can use AFR+AMR+EUR+SAS populations, or whatever combination of populations you prefer. Just make sure there are not any shared samples between the target population samples and outgroup samples, otherwise the program raises the following error:
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

When I try to run my vcf files the result is ```Error: There are i gaps with size greater than 10kbp.```
 
>When there is a gap larger than ```--MaxGapSize``` (default: 10kbp) the program raise an error. You can ignore this by setting the ```--IgnoreGaps``` flag or you can change the maximum gap size threshold by ```--MaxGapSize```.