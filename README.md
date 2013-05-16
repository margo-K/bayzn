#Bayzn
A Naive Bayesian Classifier

This project aims to do a seemingly simple task: train a classifier to make predictions about the subject of phrases based on a training corpus of phrases and their classifications and the application of Bayes Theorem

Though the math involved in applying Bayes Theorem is relatively straightforward, complications come in a real-world application in the form of various edge cases about which decisions must be made. See 'Explanations: Edge Cases' below for more information


##Contents
* __classifier.py__: 

##Getting Started
###Open Python REPL
```python
from classifier import Classifier
training_data = [('art', 'painting waterful the thing homeless art'),
				 ('sport','sport title sports thing magic johnson')
				 ('art', 'more watercolor hopes rise')
				 ('sport','basketball starts pl')]

c = Classifier(['art','sport'])
for category,text in training_data:
	c.train(category,text)

c.predict('watercolors fall from the magic sky')
>>>

```

##Examples

##Explanations

####Bayes Theorem
P(A|B) = P(B|A)*P(A) / P(B)

###Assumptions
A Bayesian classifier relies on insights from Bayes Theorem to make predictions

A **naive** Bayesian classifier simplifies the application of Bayes Theorem 
with the following assumption:

=> Assume the occurrence of one token in a text item is independent of any other

For example:
	If we are classifying news articles, we are now allowing the assumption that occurrences of the word 'Barack' in a news headline are independent of the occurrences of the word 'Obama'. In practice, this is (obviously) not true, but it allows us to simplify our calculations. 

	Note: predictions using this assumption are less precise

###Some Edge Cases
* words that do not appear in the corpus
	=> Currently, words that do not appear in the corpus are assigned a very small probability (meaning that
	its contribution to the Bayesian classifier prediction will be small_prob/small_prob = 1, i.e. it will be as if the word were not including the calculations)
* words that do appear in the corpus, but have never been encountered with a given classifier 
(leading to a prob(word,given=classifier)=0)
	=> Currently, these return a probability of 0, but should return a small probability (so that they do not wipe out the contribution of all other words in the phrase)

The problem with the above formulation is that the total probability in any given dimension will sum to > 1 because other probabilities are not being adjusted to account for part of the probability distribution being used for unknown words

Other ways that these could be dealt with:
	1. alotting a portion of the probability distribution to 'Unknown Words' and moving all lowest-probability seen words into this category
	2. Additive Smoothing/Laplacian smoothing (+1 smoothing)


##Status
- has a bug in the classification related to an edge case (see EDGE CASES above, second example)

##Notes
###TO-DO:

####Features to implement
* non-naive bayes classification (for a small 'universe')
* benchmarking to gauge how often the naive bayes classifier fails when the precise bayes classifier succeeds
* metrics to approximate the magnitude of the effect of rounding errors (see unittests)
 on predictions
* benchmarking to report on the percentage of false positives, false negatives when varying the volume of training data