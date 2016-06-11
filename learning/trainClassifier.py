from sklearn.linear_model import LogisticRegression

regularization = 0.1
classifier = LogisticRegression(C=regularization)
print(classifier.get_params())


