#!/usr/bin/env python3

import argparse, os
import arpFormat

parser = argparse.ArgumentParser(description='UWBC BRC tool for Tassel V2 report building')
parser.add_argument('--vcf', type=str,help='The path to the vcf to convert to arlequin format', required=True)
parser.add_argument('--popFile', type=str,help='A simple tab delimited file including each samples relationship expected population relationship', required=True)

args = parser.parse_args()
vcf = args.vcf
popfile = args.popFile
cwd = os.getcwd()


def findChromLine():
    count = 0
    with open(vcf,'r') as f:
        while True:
            line = f.readline()
            count = count + 1
            if line[0:6] == '#CHROM':
                return count

def processGenoField():
    pass

def parseVCF():
    pass

def main():
    chromLine = findChromLine()
    #print(chromLine)
    pass



if __name__ == '__main__':
    main()