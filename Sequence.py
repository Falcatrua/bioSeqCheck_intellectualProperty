# -*- coding: utf-8 -*-
import re
Tags = {
            '<110>': 'Applicant name',
            '<120>': 'Title of invention',
            '<130>': 'File reference',
            '<140>': 'Current patent application',
            '<141>': 'Current filing date',
            '<150>': 'Earlier patent application',
            '<151>': 'Earlier application filing date',
            '<160>': 'Number of SEQ ID NOs',
            '<170>': 'Software',
            '<210>': 'Information for SEQ ID No: x',
            '<211>': 'Length',
            '<212>': 'Type',
            '<213>': 'Organism',
            '<220>': 'Feature',
            '<221>': 'Name/key',
            '<222>': 'Location',
            '<223>': 'Other information',
            '<300>': 'Publication information',
            '<301>': 'Authors',
            '<302>': 'Title',
            '<303>': 'Journal',
            '<304>': 'Volume',
            '<305>': 'Issue',
            '<306>': 'Pages',
            '<307>': 'Date',
            '<308>': 'Database accession number',
            '<309>': 'Database entry date',
            '<310>': 'Document number',
            '<311>': 'Filing date',
            '<312>': 'Publication date',
            '<313>': 'Relevant residues in SEQ ID No: x: from to',
            '<400>': 'Sequence'
        }
Nucleotides = ['a','g','c','t','u','r','y','m','k','s','w','b','d','h','v','n', 'x']
AA = ['Ala','Cys','Asp','Glu','Phe','Gly','His','Ile','Lys','Leu','Met','Asn','Pro',
'Gln','Arg','Ser','Thr','Val','Trp','Tyr','Asx','Glx','Xaa']

class Sequence (object):
	""" Uma sequencia de DNA e seus tags """
	def __init__ (self, number):
		self._number = number 
		self._type = "" 
		self._length = ""
		self.seq = "" 
		self._seqError = []
		self.info = []
		self._infoError = []
		
	def getInfoByKey (self, key):
		value = []
		for i in self.info:
			if i[0] == key:
				value.append (i[1])
		return value

	def exportInfo_ST25 (self):
		s =  ""
		for i in self.info:
			s = s+str(i[0])+str(i[1])+" \n"
			
		return s

	def Clone (self, original):
		if original.isSequence:
			seq = Sequence(0)
			seq._number = original._number
			seq._type = original._type
			seq.info = seq.CloneArray (original.info)
			seq._infoError = seq.CloneArray (original._infoError)
			seq.seq = original.seq
			seq._seqError = seq.CloneArray (original._seqError)
			return seq
		else:
			return False

	def CloneArray (self, original):
		cloned = []
		for i in range(len(original)):
			cloned.append ([])
			for j in range(len(original[i])):
				cloned[i].append ([])
				cloned[i][j] = original[i][j]
		return cloned

	def isSequence (self):
		return True

	def checks (self):
		
		## Ajustara listagem e o campo <400>
		# copiar números para counters []
		counters = [int(s) for s in self.seq.split() if s.isdigit()] #len counters
		# retirar o primeiro elemento porque é na verdade o argumento de <400>
		self.info.append (['<400>', str(counters.pop(0))])
		self.seq = re.sub('^[\n\r\d\s]+','',self.seq)
		
		#checar contagens parciais 	
		self._type = self.checkType()
		self.checkPartialCounters()
		self._type = self.checkType()


		####checar Informações:
		for i in range(len(self.info)):
			self._infoError.append ([])
			for j in range(len(self.info[i])):
				if self.info[i][j].isdigit():
					self.info[i][j] = int (self.info[i][j])
				self._infoError[i].append([])
				self._infoError[i][j] = True
		
		#checar contagem total:
		self._length = self.checkLength()
		for i in range(len(self.info)):
			if self.info[i][0] == '<211>':
				if self._type != 'MIXED':
					if self.info[i][1] != self._length:
						self._infoError[i][1] = False
				else:
					if self.info[i][1] != self._length[0] and self.info[i][1] != self._length[1]:
						self._infoError[i][1] = False


		#checar presença de campos obrigatórios

		
	def cleanSeq (self, seq):
		seq = ''.join([i for i in seq if not i.isdigit()]) #remover counters
		seq = "\n".join([s for s in seq.split("\n") if s])
		seq = "".join([s for s in seq.splitlines(True) if s.strip("\r\n")])
		seq = seq.replace('\n', '').replace('\r', '').replace(' ','')
		seq = re.sub ('-',' ',seq)
		return seq

	def checkType (self):
		seq = self.cleanSeq(self.seq)
		Nucleotides.append (' ')
		ns = re.compile ("^["+''.join(Nucleotides)+"\s\n]+$", re.MULTILINE)
		aas = '\s*\n*)|('.join(AA)
		aas = '^(('+aas+'\s*\n*))+$'
		aas = re.compile ( aas )
			
		if ns.match (seq):
			if re.search ('u', seq):
				return 'RNA' 
			else:
				return 'DNA'
		elif aas.match (seq):
			return 'AA'
		else:
			return 'MIXED'

	def checkLength (self):
		if self._type == '':
			self._type = self.checkType()

		if self._type == 'DNA' or self._type == 'RNA':
			seq = self.cleanSeq(self.seq)
			return len(seq)

		elif self._type == 'AA':
			return ( len(re.findall('([a-z]+)\s+', self.seq)) )
		
		elif self._type == 'MIXED':
			nucs = self.seq
			aas = self.seq
			for line in self.seq.split('\n'):
				if re.search ('^[agcturymkswbdhvnx\s]+\d+$', line):
					aas = re.sub (line, ' '*len(line), aas)
				else:
					nucs = re.sub (line, ' '*len(line), nucs)
			
			nucs = self.cleanSeq (nucs)
			Lnucs = len(nucs)
			Laas = len(re.findall('([a-z]+)\s+', self.seq))
			return [Lnucs, Laas]				
		
	def checkPartialCounters (self):
		if self._type == '':
			self._type = self.checkType()

		if self._type == 'DNA':
			self.checkNucCounters(self.seq)
			
		if self._type == 'AA':
			self.checkAACounters(self.seq)
		
		if self._type == 'MIXED':
			nucs = self.seq
			aas = self.seq
			for line in self.seq.split('\n'):
				if re.search ('^[agcturymkswbdhvnx\s]+\d+$', line):
					aas = re.sub (line, ' '*len(line), aas)
				else:
					nucs = re.sub (line, ' '*len(line), nucs)
				
			cn = self.checkNucCounters (nucs)
			an = self.checkAACounters (aas)
	
	def checkAACounters (self, seq):
		aa = re.sub ('[0-9]',' ',seq)
		aa = re.sub ('-',' ',aa)
		cs = re.sub ('[a-z]', ' ', seq)
		cs = re.sub ('[A-Z]', ' ', cs)
		

		#get each line length and position
		lines_len = re.finditer ('\n',seq)
		ll = [0]
		for l in lines_len:
			ll.append (int(l.start()))	
		
		# find all counters, get positions and values
		pos_cs = []
		count = 0
		last = 0
		for m in re.finditer("-?\d+", cs):
			if count == 0:
				last = int(m.group(0))				
			#locate line
			for i in range(1,len(ll)):
				if m.start() > ll[i-1] and m.start() < ll[i]:
					break
			#  ini pos, end pos,      line pos,           value,       relative value
			diff = int(m.group(0))-last
			if int(m.group(0)) > 0 and last < 0:
				diff = diff-1
			pos_cs.append ( [m.start(), m.end(), ll[i]-ll[i-1], int(m.group(0)), diff])
			count = count+1
			last = int(m.group(0))
			
		# get each aa positions and	later a number if it has a counter	
		pos_aa = []
		count = 0
		for m in re.finditer("\w+",aa):
			pos_aa.append ( [m.start(), m.end(), m.group(0), 0])
			count = count+1

		correct = True		
		lastj = 0
		for j in range(len(pos_aa)):
			for i in range(len(pos_cs)):
				relPosC = pos_cs[i][0]-pos_cs[i][2]
				if relPosC >= pos_aa[j][0] and relPosC <= pos_aa[j][1]:
					if lastj == 0:
						lastj = j
					if lastj == j and j > 0:
						pos_aa[j][3] = j
					else:
						pos_aa[j][3] = j-lastj
					lastj = j
					#print "",pos_cs[i]," ==> ",pos_aa[j]," j: ",j#explicação
					if pos_cs[i][4] != pos_aa[j][3] and i > 0:
						self._seqError.append (["erro de contagem parcial",pos_aa[j][0],pos_aa[j][1],pos_cs[i][0],pos_cs[i][1]])
						correct = False

		return correct


	def checkNucCounters (self, seq):
		correct = True
		cumsum = 0
		lines = seq.split('\n')
		for i in range(len(lines)):
			m = re.match ('^([a-z\s]+)(\d+)$', lines[i])
			if m:
				s = re.sub (' ','',m.group(1))
				l = len(m.group(1))
				n = int(m.group(2))
				cumsum = cumsum + len(s)
				if cumsum != n:
					self._seqError.append(["ERRO: contagem parcial de nucleotideos", m.start(), m.end()])
					correct = False
			#else:
				#not a nucleotide line
		return correct
			
		
	