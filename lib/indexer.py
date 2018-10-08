import pickle, math

from .tokensParser import TokensParser

class Indexer:
	def __init__(self):
		self.index = dict()
		self.parser = TokensParser()

	def indexDocs(self, docs):
		for doc in docs:
			self.indexDoc(doc)

	#get all tokens of the document and add their occurence to the index
	#tokens are lowercased and stemmed
	#algorithm does not work with synonyms and homonyms in any way (car != automobile)
	def indexDoc(self, document):
		tokens = self.parser.getTokens(document.rawText)
		for token in tokens:
			self.addOccurence(token, document)

	#add token occurence into the index
	#inverted index is implemented so we have a dictionary of words
	#every word entry contains a list of documents that contain the word
	#occurence count in that document is also stored
	def addOccurence(self, word, doc):
		if word in self.index:
			if doc.id in self.index[word]:
				self.index[word][doc.id] = self.index[word][doc.id] + 1
			else:
				self.index[word][doc.id] = 1
				self.index[word]['count'] = self.index[word]['count'] + 1
		else:
			#as long as we iterate over a list of documents sorted by ID
			#the inverted index for every word is sorted too
			self.index[word] = {'count' : 1, doc.id : 1}

	def saveIndex(self, path):
		f = open(path, "wb")
		pickle.dump(self.index, f)
		f.close()

	@staticmethod
	def loadIndex(path):
		f = open(path, "rb")
		index = pickle.load(f)
		return index

	@staticmethod
	def computeTFIDFIndex(index, documents):
		for term in index:
			index[term]['idf'] = Indexer.computeIDF(len(index[term]) - 1, len(documents))
			for key in index[term]:
				if key == 'count' or key == 'idf':
					continue
				index[term][key] = Indexer.computeTFIDF(index[term]['idf'], index[term][key])
		return index

	@staticmethod
	def computeTF(tf):
		if tf == 0:
			return 0
		return 1 + math.log10(tf)

	@staticmethod
	def computeIDF(dft, n):
		return math.log10(n / dft)

	@staticmethod
	def computeTFIDF(idf, occurenceCount):
		tf = Indexer.computeTF(occurenceCount)
		return tf * idf
		




