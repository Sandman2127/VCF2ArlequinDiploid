# VCF2ArlequinDiploid

## Description:
A script designed to convert GBS/RAD/DNASEQ vcf data to arlequin diploid .arp format files. The program should properly convert most any vcf that uses vcf format >= 4.0 to an Arlequin 3.5.22 loadable .arp file.

## Setup
### Use >= Python 3.7:
This program has 0 dependencies, i.e. if you have base python 3.7 it will run without issue. It is possible this program will run with any >= py3 version of python, but it hasn't been extensively tested.

If you dont have python 3.7 install it via [conda](https://docs.conda.io/en/latest/miniconda.html):
```
conda create -n py37
conda install -n py37 python=3.7
```
### Build a tab delimited population file:
```
samp1 <\t> population_E
samp2 <\t> population_E
samp3 <\t> population_F
samp4 <\t> population_F
samp5 <\t> population_R
```
The population file defines the expected relationship of each sample (column 1) with population (column 2). The above is an example with 5 samples defining 3 different populations. The sample name MUST BE EXACTLY THE SAME as it is in the vcf header line starting with #CHROM<\t>POS<\t>ID... Building a tab delimited text can be done on the command line or via excel, for a further example of a functional population file see the ./testData/inputFormats/population.txt

## Usage:
### Convert your vcf into an arlequin formated diploid file (.arp):
activate the proper python environment
```
conda activate py37
```
run your vcf2ArlequinDiploid analysis
```
python /Users/deansanders/Desktop/DS_Github/VCF2ArlequinDiploid/vcf2ArlequinDiploid.py --vcf SNPs.mergedAll.vcf --popFile population.txt --splitContigs
```

#### Program Options:

* --vcf:     The path to the vcf to convert to arlequin format (VCF format >= 4.0)
* --popFile:      A two column tab delimited text file defining the expected relationship of each sample with the other samples in the population
* --splitContigs:        split the input .vcf data into several output .arp files by contig
* --debug:       run debug and print every relevant processing field for every individual in each population

### Runtime:
Not extensive... Using the longest --splitContigs method, 100k SNPs can be converted to .arp format in < 5 minutes
