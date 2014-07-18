# -*- coding: utf-8 -*-
import Sequence
from Sequence import *

import re

class SeqListing(object):
	def __init__ (self):
		self.info = []
		self._infoError = []
		self.filename = ''
		self.seqList = []

	def getInfoByKey (self, key):
		value = []
		for i in self.info:
			if i[0] == key:
				value.append (i[1])
		return value
	
	def Clear (self):
		self.info[:] = []
		self.seqList[:] = []

	def Clone (self, original):
		L = SeqListing()
		L.info = self.CloneArray (original.info)
		L._infoError = self.CloneArray (original._infoError)
		L.filename = original.filename

		for i in range(len(original.seqList)):
			seq = Sequence(0)
			L.seqList.append(seq)
			L.seqList[i] = L.seqList[i].Clone (original.seqList[i])

		return L

	def CloneArray(self, original):
		cloned = []
		for i in range(len(original)):
			cloned.append ([])
			for j in range(len(original[i])):
				cloned[i].append ([])
				cloned[i][j] = original[i][j]
		return cloned
	
	def exportInfo_ST25 (self):
		s =  ""
		for i in self.info:
			s = s+str(i[0])+str(i[1])+" \n"

			
		return s
		
	def importSeqListing (self, filename):
		self.filename = filename
		listOfTags =  file(filename,'r').read().split('<')
		seq_info = []
		for tag in listOfTags:
			matched = re.match ('(\d\d\d)>\s*(.*)\s*\n+', tag, re.DOTALL)
			if matched:
				if matched.group(1)[0] == '1':
					self.info.append ( ['<'+str(matched.group(1))+'>', str(matched.group(2))] )
				elif matched.group(1)[0] == '2':
					seq_info.append ( ['<'+str(matched.group(1))+'>', str(matched.group(2))] )
				elif matched.group(1) == '400':
					seq = Sequence(0);
					seq.info = []
					for i in range(len(seq_info)):
						seq.info.append ([])
						for j in range(len(seq_info[i])):
							seq.info[i].append ([])
							seq.info[i][j] = seq_info[i][j]
							seq.info[i][j] = seq.info[i][j].strip (' \t\n\r')						
							
					seq_info[:] = []
					seq.seq = (matched.group(2))
					self.seqList.append ( seq )
					
		for i in range(len(self.info)):
			for j in range(len(self.info[i])):
				self.info[i][j] = self.info[i][j].strip ('\n\r\t ')
				if self.info[i][j].isdigit():
					self.info[i][j] = int (self.info[i][j])
				else:
					#remover linhas em branco nas infos
					lines = self.info[i][j].split ('\n')
					self.info[i][j] = ''
					for h in range(len(lines)):
						lines[h] = lines[h].strip ('\t\n\r ')
						if not lines[h].isspace():
							self.info[i][j] = self.info[i][j] + lines[h]
						if h < len(lines)-1:
							self.info[i][j] = self.info[i][j] + '\n'				
				
		
		s = 1
		for sequence in self.seqList:
			sequence._number = s;
			sequence.checks()
			s = s+1


		self.checkSeqListing()

	def checkSeqListing (self):
		for i in range(len(self.info)):
			self._infoError.append ([])
			for j in range(len(self.info[i])):
				self._infoError[i].append([])
				self._infoError[i][j] = True
		
		# checar quantidade total de sequências na listagem
		for i in range(len(self.info)):
			if self.info[i][0] == '<160>' and len(self.seqList) != self.info[i][1]:
				self._infoError[i][1] = False



	def isSequence (self):
		return False
