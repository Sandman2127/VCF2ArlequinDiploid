#!/usr/bin/env python3

import argparse, os
import arpFormat as arp

parser = argparse.ArgumentParser(description='UWBC BRC tool for Tassel V2 report building')
parser.add_argument('--vcf', type=str,help='The path to the vcf to convert to arlequin format', required=True)
parser.add_argument('--popFile', type=str,help='A simple tab delimited file including each samples relationship expected population relationship', required=True)
parser.add_argument('--splitContigs',action="store_true",help='split output .arp files by contigs for the analysis', required=False)
parser.add_argument('--debug',action="store_true",help='run debug and print every relevant processing field for every individual in each population', required=False)

args = parser.parse_args()
vcf = args.vcf
popfile = args.popFile
cwd = os.getcwd()

def findContigs():
    checkTigs = 0
    TigList = []
    with open(vcf,'r') as f:
        while True:
            line = f.readline()
            if line:
                if checkTigs == 1:
                    TigList.append(str(line.split("\t")[0]))
                if line[0:6] == '#CHROM':
                    checkTigs = 1
            else:
                break
    contigsOut = list(set(TigList))
    return contigsOut

def findChromLine():
    count = 0
    chrLineData = []
    with open(vcf,'r') as f:
        while True:
            line = f.readline()
            count = count + 1
            if line[0:6] == '#CHROM':
                chrLineData = [line,count]
                return chrLineData

def generatePopMap():
    population_map = {}
    populations = []
    with open(popfile,'r') as popF:
        lines = popF.readlines()
        for line in lines:
            line = line.split()
            sample = str(line[0])
            samplePop = str(line[1])
            population_map[sample] = samplePop
            populations.append(samplePop)
    populationsOut = set(populations)
    popMap_popList = [population_map,populationsOut]
    return popMap_popList

def findSampCount(population,popMap):
    sampCNT = 0
    for samp,sampPop in popMap.items():
        if population == sampPop:
            sampCNT += 1
    return sampCNT

def findSampleColumn(chrLine,sample):
    pos = 0
    for field in chrLine.split("\t"):
        if str(field.strip()) == str(sample):
            return pos
        pos += 1

def processGenoField(ref,alt,geno):
    gtOut = []
    geno1 = geno[0]
    geno2 = geno[2:3]
    if geno1 == '.' and geno2 == '.':
        gtOut = ['N','N']
    elif geno1 == '0' and geno2 == '0':
        gtOut = [ref,ref]
    elif geno1 == '0' and geno2 == '1':
        gtOut = [ref,alt]
    elif geno1 == '1' and geno2 == '0':
        gtOut = [alt,ref]
    elif geno1 == '1' and geno2 == '1':
        gtOut = [alt,alt]
    return gtOut

def parseVCF(fieldPos,lineSkip,searchContig):
    if args.debug:
        print("[DEBUG]:","Contig:","Position:","refAllele:","altAllele:","genoTypeField:","fieldPos:","AlleleA","AlleleB")
    genotypeList = []
    genotypeA = "" 
    genotypeB = ""
    count = 0
    with open(vcf,'r') as f:
        while True:
            line = f.readline()
            if line:
                count += 1
                if count <= lineSkip:
                    # vcf header lines
                    pass
                else:
                    contig = str(line.split("\t")[0])
                    # Conditionals below establish running with all contigs, or the correct contig, else pass it.
                    if searchContig == "ALL" or searchContig == contig:
                        position = str(line.split("\t")[1])
                        refAllele = str(line.split("\t")[3])
                        altAllele = str(line.split("\t")[4])
                        genoTypeField = str(line.split("\t")[fieldPos])
                        # Prevents alternate allele indels from sneaking into the analysis 
                        if altAllele == '.':
                            pass
                        else:
                            alleleA,alleleB = processGenoField(refAllele,altAllele,genoTypeField)
                            genotypeA = genotypeA + alleleA
                            genotypeB = genotypeB + alleleB
                            # Only used for system debugs
                            if args.debug:
                                print("[DEBUG]:",contig,position,refAllele,altAllele,genoTypeField,fieldPos,alleleA,alleleB)
                    else:
                        pass
            else:
                break
    genotypeList = [genotypeA,genotypeB]
    return genotypeList

def buildARP(popMap,popList,contig):
    #TODO: write out the header of our arp file
    arpInst = arp.arlequinForm("Arlequin SNP analysis",len(popMap))
    if contig == "ALL":
        outputName = "contigsCombined.arp"
    else:
        outputName = contig + ".arp"
    outputARP = open(outputName,'w+')
    arpInst.writeArpHeader(outputARP)

    #TODO: parseVCF by sample group --> sample:
    chromLine,chromLineNo = findChromLine()
    for pop in popList:
        print("[STDOUT]: Converting data from the population:",str(pop))
        #TODO: write out new sample group header for each population
        nullDict = {"Must":["Pass","Something"]}
        sampCNT = findSampCount(pop,popMap)
        arpInst.writeSampleGroupData(pop,nullDict,sampCNT,"HEADER",outputARP)
        #TODO: parse for samples in the correct population and write them out as we find them
        for samp,sampPop in popMap.items():
            if pop == sampPop:
                print("[STDOUT]: Converting sample data from the sample:",str(samp),", within population:",str(sampPop))
                sampColumn = findSampleColumn(chromLine,samp)
                # if sampColumn:
                genotypeA,genotypeB = parseVCF(sampColumn,chromLineNo,contig)
                sampleData = {samp:[genotypeA,genotypeB]}
                #TODO: write out sample data for each individual in the population
                arpInst.writeSampleGroupData(pop,sampleData,sampCNT,"SAMPLE",outputARP)
                # else:
                #     print("[STDOUT]: sample data doesnt exist for sample:",str(samp),"population:",str(sampPop),"within vcf:",str(vcf))
            else:
                pass
        #TODO: write out the tail once all samples in the population complete
        arpInst.writeSampleGroupData(pop,nullDict,sampCNT,"TAIL",outputARP)

    #TODO: write out the sample group information at the end of the ARP file:
    arpInst.writeFinalSampleGroups(popList,outputARP)

def main():
    #TODO: parse popFile and find location of sample in chromLine:
    popMap,popList = generatePopMap()
    print("[STDOUT]: Your populations are:",list(popList))
    print("[STDOUT]: Your population map indicates the following mapping:",popMap)
    if args.splitContigs:
        contigList = findContigs()
        print("[STDOUT]: Splitting the output .arp files between the contig list:",contigList)
        for tig in contigList: 
            buildARP(popMap,popList,tig)
    else:
        print("[STDOUT]: Writing the entire vcf file to a single arp file")
        print("[STDOUT]: Beware, this may be too computationally intensive for the arlequin program to handle")
        buildARP(popMap,popList,"ALL")

if __name__ == '__main__':
    main()