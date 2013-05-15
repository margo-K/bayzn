import unittest
import pdb
import pprint

class Classifier:
	def __init__(self,classifiers):
		self._classifiers = classifiers # a list
		self._words = [] # also a list
		self._count = [] # will be a list of lists

	@property
	def total(self):
		return sum([x+y for x,y in self._count])

	def train(self,classification,text): # Rename the things in this to make logic clearer
		index = self._classifiers.index(classification)
		for word in text.split(): # should be able to pass in different splits
			try: 
				position = self._words.index(word)
			except ValueError:
				position = len(self._words)
				self._words.append(word)
				self._count.append([0]*len(self._classifiers))
				if len(self._words) != len(self._count): # replace with better test
					print "Uh Oh Your matching ain't working!"
			self._count[position][index]+=1

	def category_total(self,*category): #add support for intersect
		"""Category 2 must be a classifier"""
		if len(category)>1:
			classifier_index = self._classifiers.index(category[1])
			word_index = self._words.index(category[0])
			return self._count[word_index][classifier_index] # subsitute with category_total(word,index)
		elif category in self._classifiers:
			index = self._classifiers.index(category[0])
			return sum([x[index] for x in self._count])
		else:
			index = self._words.index(category[0])
			return sum(self._count[index])

	def derive_probability(self,word,classifier):
		print "Deriving from word={} classifier={}".format(word,classifier)
		return self._prob(word,given=classifier)*self._prob(classifier)/self._prob(word)
		
	def _prob(self,term,given=None):# given must be a classifier
		"""Returns the probability of getting a certain word
		*given must be an element self._classifiers"""
		if given:
			classifier_index, word_index = self._classifiers.index(given), self._words.index(term)

			denominator = self.category_total(given)
			numerator = self.category_total(term,given) # subsitute with category_total(word,index)
			print "Term:{} Numerator:{},Denominator:{},Given:{}".format(term,numerator,denominator,given)

			return numerator/float(denominator)

		else:
			denominator = self.total
			numerator = self.category_total(term)
			print "Term:{} Numerator:{},Denominator:{}".format(term,numerator,denominator)
			return numerator/float(denominator)

	def prob(self,term,isclassifier=False,given=None):
		"""Returns probability of getting a certain word. Given can be anything"""
		if term not in self._classifiers and term not in self._words: #Unencountered word
			print "{} was not found".format(term)
			return 0.000000000000001 # i.e. a small number
		if isclassifier and given in self._words: #must derive probability
			return self.derive_probability(classifier=term,word=given)
		else: # must get probability for a classifier
			return self._prob(term,given=given)

	def contribution(self,word,given_classifier):
		if word in self._words:
			contribution = self.prob(word,given=given_classifier)/self.prob(word)
			print "Contribution of {}:{}".format(word,contribution)
			return contribution
		else:
			return 1 # in case where the word is not found, ignore its contribution

	def predict(self,text):
		"""Given text, returns the probability that the text is of each classifier type"""
		for classifier in self._classifiers:
			prob = self.prob(classifier,isclassifier=True)
			for word in text.split():
				print "Current Probability {}".format(prob)
				prob*=self.contribution(word,classifier)
			print "Probability this is a {} text: {}".format(classifier,prob)

class ClassifierTests(unittest.TestCase):
	def setUp(self):
		self.c = Classifier(['alpha','beta'])
		self.c._count = {'the':[10,11],'sky':[0,7],'blue':[1,3]}

	def test_word_total(self):
		#Word Counts
		self.assertEqual(self.c.category_total('the'),10+11)
		self.assertEqual(self.c.category_total('sky'),0+7)
		self.assertEqual(self.c.category_total('blue'),1+3)

	def test_classifier_total(self):
		#Category Counts
		self.assertEqual(self.c.category_total('alpha'),10+0+1)
		self.assertEqual(self.c.category_total('beta'),11+7+3)

	def test_total(self):
		#Total Counts from Categories
		self.assertEqual(self.c.total,sum([self.c.category_total('alpha'),self.c.category_total('beta')]))

		#Total Counts from Words
		self.assertEqual(self.c.total,sum([self.c.category_total('the'),self.c.category_total('sky'),self.c.category_total('blue')]))

	def test_word_probabilities(self):
		#Absolute Probability of Words
		self.assertAlmostEqual(self.c._prob('the'),21/float(31),places=5)
		self.assertAlmostEqual(self.c._prob('sky'),7/float(31),places=5)
		self.assertAlmostEqual(self.c._prob('blue'),4/float(31),places=5)

	def test_classifier_probabilities(self):
		#Absolute Probability of Classifiers
		self.assertAlmostEqual(self.c._prob('alpha'),11/float(31),places=5)
		self.assertAlmostEqual(self.c._prob('beta'),21/float(31),places=5)

	def test_conditional_probabilities(self):
		#Conditional Probabilities of Words
		self.assertAlmostEqual(self.c._prob('the',given='beta'),11/float(21),places=5)
		self.assertAlmostEqual(self.c._prob('sky',given='alpha'),float(0),places=5) #Edge case(where prob should =0)
	
	def test_train(self):
		cat = 'alpha'
		count_before = self.c.category_total(cat)

		words = ['word1','word2','word3']

		for word in words:
			self.c.train(cat,word)

		count_after = self.c.category_total(cat)

		self.assertEqual(len(words),count_after-count_before)

	def test_counts(self):
		training_data = [('art', 'painting waterful thing homeless art'),
				 ('sport','sport title sports thing magic johnson'),
				 ('art', 'more watercolor hopes rise'),
				 ('sport','basketball starts pl')]
		c = Classifier(['art','sport'])
		for category,text in training_data:
			c.train(category,text)

		calculated_counts = dict(zip(c._words, c._count))

		real_counts = {'painting':[1,0],
					   'waterful':[1,0],
					   'thing':[1,1],
					   'homeless':[1,0],
					   'art':[1,0],
					   'sport':[0,1],
					   'title':[0,1],
					   'sports':[0,1],
					   'magic':[0,1],
					   'johnson':[0,1],
					   'more':[1,0],
					   'watercolor':[1,0],
					   'hopes':[1,0],
					   'rise':[1,0],
					   'basketball':[0,1],
					   'starts':[0,1],
					   'pl':[0,1]}
		self.assertEqual(calculated_counts,real_counts)

	def test_probabilities(self):
		training_data = [('art', 'painting waterful thing homeless art'),
				 ('sport','sport title sports thing magic johnson'),
				 ('art', 'more watercolor hopes rise'),
				 ('sport','basketball starts pl')]
		c = Classifier(['art','sport'])
		for category,text in training_data:
			c.train(category,text)

		expected_probs = {'basketball': 1/18,
						 'art':1/18,
						 'johnson': 1/18,
						 'title': 1/18,
						 'starts':1/18,
						 'rise':1/18,
						 'sports':1/18,
						 'watercolor':1/18,
						 'thing': 2/18,
						 'pl': 1/18,
						 'homeless': 1/18,
						 'hopes': 1/18,
						 'magic': 1/18,
						 'sport': 1/18,
						 'painting': 1/18,
						 'waterful': 1/18,
						 'more':1/18} # 17 unique words, with one word appearing twice = 18 'words'


if __name__ == '__main__':
	training_data = [('art', 'painting waterful thing homeless art'),
				 ('sport','sport title sports thing magic johnson'),
				 ('art', 'more watercolor hopes rise'),
				 ('sport','basketball starts pl')]

	k = Classifier(['art','sport'])
	for category,text in training_data:
		k.train(category,text)
	print "Classifiers:{}, \nWords:".format(k._classifiers)
	words = dict(zip(k._words, k._count))
	pprint.pprint(words)
	# pprint.pprint(map(k.prob,k._words))
	# #pdb.set_trace()
	# pprint.pprint(zip(c._words,c._count))
	k.predict('watercolor fall from magic sky')
	# unittest.main()





























