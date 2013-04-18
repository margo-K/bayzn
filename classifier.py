import unittest
import pdb

class Classifier:
	def __init__(self,classifiers):
		self._classifiers = classifiers
		self._count = {}

	@property
	def total(self):
		return sum(map(self.category_total,self._count)) # Note: map from a dictionary means a different order, but it doesn't matter in this case

	def train(self,classification,text):
		index = self._classifiers.index(classification)
		for word in text.split(): # should be able to pass in different splits
			counts = self._count.setdefault(word,[0]*len(self._classifiers))
			counts[index]+=1

	def category_total(self,category):
		count = 0
		if category in self._classifiers:
			index = self._classifiers.index(category)
			for word in self._count:
				count+=self._count[word][index]
		else:
			count = sum(self._count[category])
		return count


	def _prob(self,category,given=None):
		"""Returns the probability of getting a certain word"""
		if not given:
			denominator = self.total
			count = self.category_total(category)
		else: 
			denominator = self.category_total(given) # Not quite correct (cause we're not counting the ones in that category)
			index = self._classifiers.index(category)
			count = self._count[category][index]
		# assert(if given: category in self._count) # i.e. if a given is specified, the category is a word instead
		# of a classifier
		return count/float(denominator)

	def predict(self,text):
		"""Given text, returns the probability that the text is of each classifier type"""
		pass


class ClassifierTests(unittest.TestCase):
	def setUp(self):
		self.c = Classifier(['alpha','beta'])
		self.c._count = {'the':[10,11],'sky':[0,7],'blue':[1,3]}

	def test_category_total(self):
		#Word Counts
		self.assertEqual(self.c.category_total('the'),10+11)
		self.assertEqual(self.c.category_total('sky'),0+7)
		self.assertEqual(self.c.category_total('blue'),1+3)

		#Category Counts
		self.assertEqual(self.c.category_total('alpha'),10+0+1)
		self.assertEqual(self.c.category_total('beta'),11+7+3)

		#Total Counts
		self.assertEqual(self.c.total,sum([self.c.category_total('alpha'),self.c.category_total('beta')]))
		self.assertEqual(self.c.total,sum([self.c.category_total('the'),self.c.category_total('sky'),self.c.category_total('blue')]))

	def test_probabilities(self):
		#Absolute Probability of Words
		self.assertEqual(self.c._prob('the'),21/float(31))
		self.assertEqual(self.c._prob('sky'),7/float(31))
		self.assertEqual(self.c._prob('blue'),4/float(31))

		#Absolute Probability of Classifiers
		self.assertEqual(self.c._prob('alpha'),11/float(31))
		self.assertEqual(self.c._prob('beta'),21/float(31))

		#Conditional Probabilities of Words
		self.assertEqual(self.c._prob('the',given='beta'),11/float(21))
		self.assertEqual(self.c._prob('sky',given='alpha'),float(0)) #Edge case(where prob should =0)

if __name__ == '__main__':
	unittest.main()









































# import pdb
# C = {} # C['word'][0] = number of articles of type 0 that word is in
# # count = {} #count[classifier] = number of articles of type classifier

# classifiers = ('art','sport')
# count = {classifier:0 for classifier in classifiers}


# def tokenize(string):
# 	"""Return a list of tokens from a given string"""
# 	return string.split()

# def plusdatapoint(string,classification):
# 	count[classification]+=1
# 	print "entering data point calc C: {}\ncount:{}".format(C,count)
# 	for token in set(tokenize(string)):
# 		wordentry = C.setdefault(token,{classification: 0}) 
# 		# print "Word entry: {}".format(wordentry)
# 		item = wordentry.setdefault(classification,0)
# 		item+=1
# 	return C, count

# def get_probability(word,classifier):
# 	"""Returns P(article has word in it|article of of type classifer), i.e. P(word|A) for arts article"""
# 	classindex = i[classifier]
# 	wordcount = C[word][classindex]
# 	typecount = count[classindex]

# 	return wordcount/typecount

# def classify(wordinarticle):
# 	for classifier in i:
# 		print "{classifier}: ".format(get_probability(wordinarticle,classifier)*(count[classifier]/sum(count)))


# # def classify(string,classifier):
# # 	tokens = tokenize(string)
# # 	for token in tokens:
# # 		P[token][c[classifier]]+=1
# # 		count[c[classifier]] += 


# if __name__ == '__main__':
	
# 	titles = [('art', 'painting waterful the thing homeless art'),('sport','sport title sports thing magic johnson')]
# 	for classifier,headline in titles:
# 		C, count = plusdatapoint(headline,classifier)

# 	print "All done: "
# 	print "count: {}".format(count)
# 	print "C {}".format(C)
# 	# #pdb.set_trace()


