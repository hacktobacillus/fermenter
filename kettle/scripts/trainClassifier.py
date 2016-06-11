from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from kettle.scripts.formatData import BeerMLData
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
        self.classifier = MultinomialNB()

class SVCBeerClassifier(Classifier):

    def __init__(self):
        Classifier.__init__(self)
        self.classifier = SVC(kernel='linear',probability=True)


class LRBeerClassifier(Classifier):

    def __init__(self,regularization=100.0):
        Classifier.__init__(self)
        self.regularization = regularization
        self.classifier = LogisticRegression(C=self.regularization)



def test_run():
    import matplotlib.pyplot as plt
    from matplotlib.cm import jet

    #beers_i_like = ['samael-s','rumpkin','the-beast','out-of-bounds-stout','baltic-porter']
    #beers_i_dont = ['joe-s-pils','raja','ipa','summer-s-day-ipa','dry-hopped-ipa','dugana']
    beers_i_like = ['samael-s']
    beers_i_dont = ['ipa']

    

    classifier = LRBeerClassifier(100.)
    #classifier = NBBeerClassifier()
    #classifier = SVCBeerClassifier()
    classifier.train(beers_i_like,beers_i_dont)

    
    Y = classifier.beer_data.project()
    
    plt.figure()
    plt.gca().set_axis_bgcolor('k')

    vals = []
    for i,beer in enumerate(classifier.beer_data):
        k = beer['name']
        val = classifier.classify(beer['id'])
        vals.append( (val,k))

        color = jet(int(255*val))
        #'''
        if val > 0.5:
            plt.text(Y[i,0],Y[i,1],k,color=color)
            plt.plot([Y[i,0]],[Y[i,1]],'go',mec=color,mfc=color)
        else:
            plt.text(Y[i,0],Y[i,1],k,color=color)
            plt.plot([Y[i,0]],[Y[i,1]],'ro',mec=color,mfc=color)
        #'''
    vals.sort()
    for val in vals:
        print(val)
    plt.show()

