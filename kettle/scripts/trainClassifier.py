from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from formatData import BeerMLData
import numpy as np


class Classifier:
    def __init__(self):
        self.beer_data = BeerMLData()
        self.beer_data.from_model()
        self.beer_data.create_beer_mapping()
        self.beer_data.get_mapping_asarray()

    def get_features(self,pos,neg):
        pos = [self.beer_data.map_beer(beer) for beer in pos]
        neg = [self.beer_data.map_beer(beer) for beer in neg]
       

        X = np.vstack((np.array(pos),np.array(neg)))
        y = np.concatenate((np.ones(len(pos)),np.zeros(len(neg))))
        return X,y

    def train(self,pos,neg):
        X,y = self.get_features(pos,neg)
        self.classifier.fit(X,y)

    def classify(self,beer_id):
        mapped = self.beer_data.map_beer(beer_id)
        return self.classifier.predict_proba(np.array([mapped]))[0][1]
 
class NBBeerClassifier(Classifier):

    def __init__(self):
        Classifier.__init__(self)
        self.classifier = GaussianNB()

class LRBeerClassifier(Classifier):

    def __init__(self,regularization=100.0):
        Classifier.__init__(self)
        self.regularization = regularization
        self.classifier = LogisticRegression(C=self.regularization)



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.cm import jet

    beers_i_like = ['samael-s','rumpkin','the-beast','out-of-bounds-stout']
    beers_i_dont = ['joe-s-pils','raja','ipa']

    

    #classifier = LRBeerClassifier()
    classifier = NBBeerClassifier()
    classifier.train(beers_i_like,beers_i_dont)

    
    Y = classifier.beer_data.project()
    
    plt.figure()
    plt.gca().set_axis_bgcolor('k')

    for i,beer in enumerate(classifier.beer_data):
        k = beer['name']
        val = classifier.classify(beer['id'])
        print (k,val)

        color = jet(int(255*val))
        #'''
        if val > 0.5:
            plt.text(Y[i,0],Y[i,1],k,color=color)
            plt.plot([Y[i,0]],[Y[i,1]],'go',mec=color,mfc=color)
        else:
            plt.text(Y[i,0],Y[i,1],k,color=color)
            plt.plot([Y[i,0]],[Y[i,1]],'ro',mec=color,mfc=color)
        #'''
    plt.show()

