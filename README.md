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

ntains the words in this headline, given that it is a sports article

###Assumptions
A Bayesian classifier relies on insights from Bayes Theorem to make predictions

A **naive** Bayesian classifier simplifies the application of Bayes Theorem 
with the following assumption:

=> Assume the occurence of one token in a text item is independent of any other

For example:
	If we are classifying news articles, we are now allowing the assumption that occurrences of the word 'Barack' in a news headline are independent of the occurrences of the word 'Obama'. In practice, this is (obviously) not true, but it allows us to simplify our calculations. 

	Note: predictions using this assumption are less precise

###Some Edge Cases
* words that do not appear in the corpus
* words that do appear in the corpus, but have never been encountered with a given classifier (leading to a prob(word,given=classifier)=0)


##Status
- has a bug in the classification related to an edge case (see EDGE CASES above, second example)

##Notes
###TO-DO:
* Implement API described above
* write explanations using a simpler case

####Features to implement
* non-naive bayes classification (for a small 'universe')
* benchmarking to gauge how often the naive bayes classifier fails when the precise bayes classifier succeeds
* metrics to approximate the magnitude of the effect of rounding errors (see unittests)
 on predictions
* benchmarking to report on the percentage of false positives, false negatives when varying the volume of training data