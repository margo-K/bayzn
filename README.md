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

```

###Examples

###Explanations

###Status
###Notes
###TO-DO:
* Implement API described above