
FAQ – frequently asked questions
=============
<h4>Q: Do I have to add random samples?</h4> 

When the favored mutation is near fixation (or fixed) the performance of the iSAFE decays. As we discussed in the [online methods](https://www.nature.com/articles/nmeth.4606#methods) and [Supplementary Figure 3e](https://www.nature.com/articles/nmeth.4606/figures/6), adding random sample from outgroup populations dramatically improves the iSAFE performance. Given proper outgroup populations (using ```--vcf-cont```and ```--sample-cont``` arguments) the program calculates Eq. 6 ([online methods](https://www.nature.com/articles/nmeth.4606#methods)) and automatically decides whether random samples are required or not. As an example see the Scenario 3 of the [Demo 2](https://github.com/alek0991/iSAFE#demo-2-input-in-vcf-format).  

<h4>Q: Which outgroup populations should we use?</h4> 

In the [online methods](https://www.nature.com/articles/nmeth.4606#methods) of the iSAFE paper we mentioned that "in testing on the phase 3 1000GP data, we chose outgroup samples from non-target 1000GP populations." For example for East-Asian sub-populations (like CHB+JPT) you can use AFR+AMR+EUR+SAS populations, or whatever combination of populations you prefer. Just make sure there are not any shared samples between the target population samples and outgroup samples, otherwise the program raises the following error:

   ```sh
   --sample-case and/or --sample-cont have shared/duplicated samples.
   ```  
Also make sure to use the rigth format the [sample ID file](https://github.com/alek0991/iSAFE/blob/master/sample_ID_format.md). 
<h4>Q: Can we change the default values of RandomSampleRate or MaxFreq parameters?</h4>

The default values for ```RandomSampleRate=0.10``` and for ```MaxFreq=0.95```, and it is fine to change them. As a rule of thumb, I usually set ```MaxFreq = (1-RandomSampleRate/2)``` , to minimize the noise due to adding outgroups.

<h4>Q: Should we change the default value of MaxRank parameter?</h4>

In most of the cases, the default value for ```MaxRank=15``` works just fine and the favored mutation is included. By setting ```MaxRank=300``` ( or whatever value &#8805; ``` WINDOW```, default: 300) you make sure that you are not missing the favored mutation 100%, however the computation time increases linearly with this parameter.

<h4>Q: When I try to run my vcf files the result is "ValueError: There are i gaps with size greater than 10kbp."</h4>
 
When there is a gap larger than ```--MaxGapSize``` (default: 10kbp) the program raise an error. You can ignore this by setting the ```--IgnoreGaps``` flag or you can change the maximum gap size threshold by ```--MaxGapSize```.