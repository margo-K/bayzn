import unittest
import pdb

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

	def category_total(self,category): #add support for intersect
		if category in self._classifiers:
			index = self._classifiers.index(category)
			return sum([x[index] for x in self._count])
		else:
			index = self._words.index(category)
			return sum(self._count[index])

	def derive_probability(self,category,givend):
		return self._prob(givend,given=category)*self._prob(category)/self._prob(given)
		


	def _prob(self,category,given=None,notfoundfn=lambda : 1):# given must be a classifier
		"""Returns the probability of getting a certain word
		*given can be any element of self._classifiers"""
		if category not in self._classifiers and category not in self._words:
			return notfoundfn()
		if not given:
			denominator = self.total
			numerator = self.category_total(category)
			return numerator/float(denominator)
		else:
			if given in self._classifiers:
				classifier_index = self._classifiers.index(given)
				denominator = self.category_total(given)
	
				word_index = self._words.index(category)
				numerator = self._count[word_index][classifier_index]
				return numerator/float(denominator)
			else:
				return self.derive_probability(self,category,givend=given) # what's going on here

	def predict(self,text):
		"""Given text, returns the probability that the text is of each classifier type"""
		for classifier in self._classifiers:
			prob = self._prob(classifier)
			for word in text.split():
				wordprob = self._prob(word,given=classifier)/self._prob(word)
				print "{}: {}".format(word,wordprob)
				prob*=wordprob

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

if __name__ == '__main__':
	training_data = [('art', 'painting waterful the thing homeless art'),
				 ('sport','sport title sports thing magic johnson'),
				 ('art', 'more watercolor hopes rise'),
				 ('sport','basketball starts pl')]
	c = Classifier(['art','sport'])
	for category,text in training_data:
		c.train(category,text)
	print "Classifiers:{}, Words: {}, Counter: {}".format(c._classifiers,c._words, c._count)
	c.predict('watercolors fall from the magic sky')
	# unittest.main()





























