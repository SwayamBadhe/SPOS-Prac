import re
pattern = re.compile(
	r'\(\'([A-Z]{,2})\',\s(\d+)\)'
)

class pass2:
	def __init__(self):
		self.ICFile = open("intermediateCode.txt", "r")
		self.litTableFile = open("literalTable.txt", "r")
		self.symbolTableFile = open("symbolTable.txt", "r")
		self.outputFile = open("output.txt", "w")
		self.literalTable = {}
		self.symbolTable = {}
		
	def convertToString(self, string):
		string = str(string)
		if len(string) == 1:
			return "00" + string
		elif len(string) == 2:
			return "0" + string
		else:
			return string
		
	def readSymbolTable(self):
		print("\nSYMBOL TABLE")
		for line in self.symbolTableFile.readlines():
			line = line.split("\t")
			index = int(line[0])
			location = int(line[2])
			self.symbolTable[index] = location
			print(index, location, sep = "\t")
		print("\n")
	
	def readLiteralTable(self):
		print("\nLITERAL TABLE")
		for line in self.litTableFile.readlines():
			line = line.split("\t")
			index = int(line[0])
			location = int(line[2])
			self.literalTable[index] = location
			print(str(index) + "\t" + str(location))
		print("\n")
	
	def parseFile(self):
		self.readSymbolTable()
		self.readLiteralTable()
		
		print("MACHINE CODE")
		print("LC\tOPCODE\tOP1\tOP2\n")
		
		for line in self.ICFile.readlines():
			line = line.strip("\n").split("\t")
			find = pattern.search(line[0])
			
			if find.group(1) == "IS" or find.group(1) == "DL":
				lineToParse = ""
				location = line[-2]
				lineToParse += location + "\t"
				
				if find.group(1) == "IS":
					lineToParse += self.convertToString(find.group(2)) + "\t"
					
					if find.group(2) == "10" or find.group(2) == "9":
						find = pattern.search(line[1])
						key = int(find.group(2))
						lineToParse += "000" + "\t" + self.convertToString(self.symbolTable[key]) + "\n"
					
					elif find.group(2) == "0":
						lineToParse += "000" + "\t" + "000" + "\n"	
						
					else:
						find = pattern.search(line[1])
						lineToParse += self.convertToString(find.group(2)) + "\t"
						
						# look in symbol table
						find = pattern.search(line[2])
						if find.group(1) == "S":
							key = int(find.group(2))
							lineToParse += self.convertToString(self.symbolTable[key]) + "\n"
							
						# look in literal table
						elif find.group(1) == "L":
							key = int(find.group(2))
							lineToParse += self.convertToString(self.literalTable[key]) + "\n"
				
				# DL		
				else:
					if find.group(2) == "1":
						lineToParse += "000" + "\t" + "000" + "\t"
						find = pattern.search(line[1])
						lineToParse += self.convertToString(find.group(2)) + "\n"
					else:
						lineToParse += "000" + "\t" + "000" + "\t" + "000" + "\n"
				
			else:
				continue
			
			print(lineToParse, end = "")
			self.outputFile.write(lineToParse)
		
		self.outputFile.close()
		self.litTableFile.close()
		self.symbolTableFile.close()
		
obj = pass2()
obj.parseFile()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
