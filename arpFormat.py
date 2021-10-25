#!/usr/bin/env python3

class arlequinForm:
    def __init__(self,title,totalSamp):
        self.sampTitle = title
        self.noSamp = totalSamp
        self.genoData = 1
        self.gameticPhase = 0
        self.dType = 'DNA'
        self.missData = '\'N\''
        self.locusSep = 'NONE'
        self.profileString = "[Profile]\n" + "Title=" + "\"" + str(self.sampTitle) + "\"" + "\n" + "NbSamples=" + str(self.noSamp) + "\n" + "GenotypicData=" + str(self.genoData) + "\n" + "GameticPhase=" + str(self.gameticPhase) + "\n" + "DataType=" + str(self.dType) + "\n" + "MissingData=" + self.missData + "\n" + "LocusSeparator=" + str(self.locusSep) + "\n" + '[Data]' + "\n"
        # [Profile]
        #  Title="SNP data"
        #  NbSamples=4
        #  GenotypicData=1
        # GameticPhase=0
        #  DataType=DNA
        # MissingData='N'
        # LocusSeparator=NONE
        # [Data]

    def writeArpHeader(self,outputFileObject):
        outputFileObject.write(self.profileString)

    def writeSampleGroupData(self,groupName,SampData,SampCount,writeObj,outputFileObject):
        if writeObj == "HEADER":
            header = "[[Samples]]" + "\n" + "SampleName=" + "\"" + str(groupName) + "\"" + "\n" + "SampleSize=" + str(SampCount) + "\n" + "SampleData= {\n"
            outputFileObject.write(header)
        elif writeObj == "TAIL":
            tail = "\n}\n"
            outputFileObject.write(tail)
        elif writeObj == "SAMPLE":
            sampleLine = ""
            for sample,genotype in SampData.items():
                sampleLine = sampleLine + "\t" + str(sample) + "\t" + str(1) + "\t" + str(genotype[0]) + "\n" + "\t\t\t" + str(genotype[1]) + "\n"
            outputFileObject.write(sampleLine)
        # tail = "\n}\n"
        #  [[Samples]]
        # SampleName="Ontario"
        # SampleSize=6
        # SampleData= {
        # 	ONT0102D	1	AAATGAAGTGGGAGGTTCCGG
        # 			AACTGAAGTGGGAGGTTCCGG
        # 	ONT0402D	1	AACTGAAGTGGGAGGTTCCGG
        # 			AACTGAAGTGGGAGGTTCCGG
        # 	ONT0702	1	AAATGAAGTTGGACGTTTCGA
        # 			AAATGAAGTTGGACGTTTCGA
        # 	ONT0902D	1	AAATGAAGTTGGACGTTTCGG
        # 			AAATGAAGTTGGACGTTTCGG
        # 	ONT1102	1	AAATGAAGTTGGACGTTTCGA
        # 			AAATGAAGTTGGACGTTTCGA
        # 	ONT1102D	1	AACTGAAGTTGGACGTTTCGG
        # 			AACTGAAGTTGGACGTTTCGG

        #}
        
    def writeFinalSampleGroups(self,groups,outputFileObject):
        header = '[[Structure]]' + '\n' + 'StructureName="A group of ' + str(len(groups)) + ' populations"' + "\n" + 'NbGroups=1' + "\n" + "Group= {" + "\n"
        FinalGroups = ""
        for group in groups:
            FinalGroups = FinalGroups + "\"" + str(group) + "\"" + "\n"
        FinalGroupString = header + FinalGroups + "}" + "\n"
        outputFileObject.write(FinalGroupString)

        # [[Structure]]
        #  StructureName="A group of n populations analyzed for DNA"
        #  NbGroups=1
        #  Group= {
        # "Alberta"
        # "BC"
        # "Quebec"
        # "Ontario"
        #  }