#Bayzn
A (Currently) Naive Bayes Classifier


###Contents
* __classifier.py__: 

###Getting Started
```
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

###Examples

###Explanations

####Bayes Theorem
P(A|B) = P(B|A)*P(A) / P(B)

#####Derivation

#####Translated into this Domain
Example application: classifying headlines into 'sports' or 'arts' categories

unit = headline
A = {'sports' headlines or 'arts headlines'}
B = {set of all words in the headlines}

headline = 'Kandinsky sells for millions'
category_being_examined = 'sports'

P(A|B) = probability the the headline is for a sports article, given it has the words 'Kandinsky','sells','for' & 'millions' in it

P(A) = probability a random headline is a sports article
P(B) = probability that a random headline contains the words 'Kandinsky','sells','for','millions' in it

P(B|A) = probability that a random headline contains the words in this headline, given that it is a sports article




####Assumptions
A Bayesian classifier relies on insights from Bayes Theorem to make predictions

A **naive** Bayesian classifier simplifies the application of Bayes Theorem 
with the following assumption:

=> Assume the occurence of one token in a text item is independent of any other

For example:
	If we are classifying news articles, we are now allowing the assumption that occurences of the word 'Barack' in a news headline are independent of the occurences of the word 'Obama'. In practice, this is (obviously) not true, but it allows us to simplify our calculations. 

	Note: predictions using this assumption are less precise



###Status
###Notes
####TO-DO:
* Implement API described above
* write explanations using a simpler case

####Features to implement
* non-naive bayes classification (for a small 'universe')
* benchmarking to gauge how often the naive bayes classifier fails when the precise bayes classifier succeeds
* metrics to approximate the magnitude of the effect of rounding errors (see unittests)
 on predictions
* benchmarking to report on the percentage of false positives, false negatives when varying the volume of training data