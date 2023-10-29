from os import sep, write
# sep -> separator / 
# write -> I/O

class Mnemonics:
    def __init__(self):
        self.AD = {"START": 1, "END": 2, "ORIGIN": 3, "EQU": 4, "LTORG": 5}
        self.RG = {"AREG": 1, "BREG": 2, "CREG": 3, "DERG": 4}
        self.DL = {"DC": 1, "DS": 2}
        self.IS = {"STOP": 0, "ADD": 1, "SUB": 2, "MULT": 3, "MOVER": 4,
                   "MOVEM": 5, "COMP": 6, "BC": 7, "DIV": 8, "READ": 9, "PRINT": 10
                   }
        self.CC = {"LT": 1, "LE": 2, "EQ": 3, "GT": 4, "GE": 5, "ANY": 6}

    def getClassType(self, string):
        if string in self.AD:
            return "AD"
        elif string in self.CC:
            return "CC"
        elif string in self.DL:
            return "DL"
        elif string in self.IS:
            return "IS"
        elif string in self.RG:
            return "RG"
        else:
            return ""

    def getMachineCode(self, string):
        if string in self.AD:
            return self.AD[string]
        elif string in self.CC:
            return self.CC[string]
        elif string in self.DL:
            return self.DL[string]
        elif string in self.IS:
            return self.IS[string]
        elif string in self.RG:
            return self.RG[string]
        else:
            return -1
            
class pass1:
    def __init__(self):
        # Initialize data structures
        self.lookup = Mnemonics()
        self.symbolTable = {}  # dict
        self.literalTable = {}
        self.litTableIndex = 0
        self.poolTable = [0]
        self.IC = []  # list
        self.location = 0
        self.litTablePtr = 0
        
        # Open files for output
        self.inputFile = open("input.txt", "r")
        self.literalTablefile = open("literalTable.txt", "w")
        self.symbolTablefile = open("symbolTable.txt", "w")
        self.poolTableFile = open("poolTable.txt", "w")
        self.ICFile = open("intermediateCode.txt", "w")

    def calculateLocation(self, string):
        if "+" in string:
            string = string.split("+")
            return self.symbolTable[string[0]] + int(string[1])
        elif "-" in string:
            string = string.split("-")
            return self.symbolTable[string[0]] - int(string[1])
        else:
            return self.symbolTable[string]
        
    def parseFile(self): 
        for line in self.inputFile.readlines():
            self.IC.append([])
            line = line.strip("\n")
            line = line.split("\t")

        # identify labels
            if line[0] != "":
                if line[0] in self.symbolTable:
                    self.symbolTable[line[0]] = self.location
                else:
                    # new entry
                    self.symbolTable[line[0]] = self.location

            if line[1] == "START": 
                self.location = int(line[2])
                self.IC[-1].append(('AD', 1))
                self.IC[-1].append(("C", int(line[2])))
            # "LTORG" is used to indicate that literal constants defined 
            # within the program should be assigned memory addresses
            elif line[1] == "LTORG":
                for i in range(self.poolTable[-1], len(self.literalTable)):
                    self.literalTable[i][1] = self.location
                    self.IC[-1].append(("AD", 5))
                    self.IC[-1].append(("C", self.literalTable[i][0]))
                    self.IC[-1].append(self.location)
                    self.location += 1
                    self.litTablePtr += 1
                    if (i < len(self.literalTable) - 1):
                        self.IC.append([])
                self.poolTable.append(self.litTablePtr)
            elif line[1] == "ORIGIN":
                self.location = self.calculateLocation(line[2])
                self.IC[-1].append(("AD", 3))
                self.IC[-1].append(("C", self.location))
            elif line[1] == "EQU":
                newlocaiton = self.calculateLocation(line[2])
                self.symbolTable[line[0]] = newlocaiton
                self.IC[-1].append(("AD", 4))
                self.IC[-1].append(("C", newlocaiton))
            elif line[1] == "DC":
                self.IC[-1].append(("DL", 1))
                self.IC[-1].append(("C", int(line[2])))
                self.IC[-1].append(self.location)
                self.location += 1
            # allocate the requested range of memory for data items
            elif line[1] == "DS":
                self.IC[-1].append(("DL", 2))
                self.IC[-1].append(("C", int(line[2])))
                self.IC[-1].append(self.location)
                self.location += int(line[2])
            elif line[1] == "STOP":
                self.IC[-1].append(("IS", 0))
                self.IC[-1].append(self.location)
                self.location += 1
            elif line[1] == "END":
                self.IC[-1].append(("AD", 2))
                if self.litTablePtr != len(self.literalTable):
                    for i in range(self.poolTable[-1], len(self.literalTable)):
                        self.IC.append([])
                        self.literalTable[i][1] = self.location
                        # literals are constants
                        self.IC[-1].append(("DL", 1))
                        self.IC[-1].append(("C", self.literalTable[i][0]))
                        self.location += 1
                        self.litTablePtr += 1
                    self.poolTable.append(self.litTablePtr)
            elif line[1] == "PRINT":
                self.IC[-1].append(("IS", 10))
                symTabKeys = list(self.symbolTable.keys())
                self.IC[-1].append("S", symTabKeys.index(line[2]))
                self.IC[-1].append(self.location)
                self.location += 1
            # value assigned in pass 2
            elif line[1] == "READ":
                self.IC[-1].append(("IS", 9))
                self.symbolTable[line[2]] = None
                symTabKeys = list(self.symbolTable.keys())
                self.IC[-1].append("S", symTabKeys.index(line[2]))
                self.IC[-1].append(self.location)
                self.location += 1
            # Conditional Branch
            elif line[1] == "BC":
                self.IC[-1].append(("IS", 7))
                classType = self.lookup.getClassType(line[2])
                machineCode = self.lookup.getMachineCode(line[2])
                self.IC[-1].append((classType, machineCode))
                if line[3] not in self.symbolTable:
                    self.symbolTable[line[3]] = None
                symTabKeys = list(self.symbolTable.keys())
                self.IC[-1].append("S", symTabKeys.index(line[2]))
                self.IC[-1].append(self.location)
                self.location += 1
            else:
                # Opcode
                classType = self.lookup.getClassType(line[1])
                machineCode = self.lookup.getMachineCode(line[1])
                self.IC[-1].append((classType, machineCode))

                # Operand 1
                classType = self.lookup.getClassType(line[2])
                machineCode = self.lookup.getMachineCode(line[2])
                self.IC[-1].append((classType, machineCode))

                # Operand 2
                if "=" in line[3]:
                    constant = int(line[3].strip("=").strip("'"))
                    self.literalTable[self.litTableIndex] = [constant, None]
                    self.IC[-1].append(("L", self.litTableIndex))
                    self.IC[-1].append(self.location)
                    self.litTableIndex += 1
                else:
                    if line[3] in self.symbolTable:
                        symTabKeys = list(self.symbolTable.keys())
                        self.IC[-1].append(("S", symTabKeys.index(line[3])))
                        self.IC[-1].append(self.location)
                    else:
                        self.symbolTable[line[3]] = None
                        symTabKeys = list(self.symbolTable.keys())
                        self.IC[-1].append(("S", symTabKeys.index(line[3])))
                        self.IC[-1].append(self.location)

                self.location += 1

        self.printLiteralTable()
        self.printSymbolTable()
        self.printPoolTable()
        self.printIntermdeiateCode()
    
    def printLiteralTable(self):
        print("\nLITERAL TABLE")
        for i in range(len(self.literalTable)):
            line = str(i) + "\t" + str(self.literalTable[i][0]) + "\t" + str(self.literalTable[i][1]) + "\n"
            self.literalTablefile.write(line)
            print(line, end = "")
        self.literalTablefile.close()
        print("\n")
        
    def printSymbolTable(self):
        print("\nSYMBOL TABLE")
        for i, item in enumerate(self.symbolTable):
            line = str(i) + "\t" + str(item) + "\t" + str(self.symbolTable[item]) + "\n"
            self.symbolTablefile.write(line)
            print(line, end = "")
        self.symbolTablefile.close()
        print("\n")

    def printPoolTable(self):
        print("\nPOOL TABLE")
        for i in range(len(self.poolTable)):
            self.poolTableFile.write(str(self.poolTable[i]) + "\n")
            print(self.poolTable[i])

    def printIntermdeiateCode(self):
        print("\nINTERMEDIATE CODE")
        for item in self.IC:
            line = ""
            for i in range(len(item)):
                line += str(item[i])
                if i != len(item):
                    line += "\t"
            line += "\n"
            self.ICFile.write(line)
            print(line, end = "")
        self.ICFile.close()

obj = pass1()
obj.parseFile()