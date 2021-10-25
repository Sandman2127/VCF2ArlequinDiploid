# VCF2ArlequinDiploid

## Description:
A script designed to convert GBS/RAD/DNASEQ vcf data to arlequin diploid .arp format files. The program should properly convert most any vcf that uses vcf format >= 4.0 to an Arlequin 3.5.22 loadable .arp file.

## Setup
### Use >= Python 3.7:
This program has 0 dependencies, i.e. if you have base python3.7 it will run without issue. It is possible this program will run with any >= py3 version of python, but it hasn't been extensively tested.

If you dont have python 3.7 install it via [conda](https://docs.conda.io/en/latest/miniconda.html):
```
conda create -n py37
conda install -n py37 python=3.7
```
### Build a simple tab delimited population file:
```
samp1 <\t> population_E
samp2 <\t>  population_E
samp3 <\t> population_F
samp4 <\t> population_F
```
This can be done on the command line or excel, for a further example population file see the ./testData/inputFormats/population.txt

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

#### Pipeline Options:

* --vcf:     The path to the vcf to convert to arlequin format
* --popFile:      A simple tab delimited file including each samples relationship expected population relationship (see population file)
* --splitContigs:        split output .arp files by contigs for the analysis
* --debug:       run debug and print every relevant processing field for every individual in each population

### Runtime:
Not extensive... Using the longest --splitContigs method, 100k SNPs can be converted to .arp format in < 5 minutes
