from sklearn.linear_model import LogisticRegression
from formatData import BeerMLData
import numpy as np

class LRBeerClassifier:
    def __init__(self):
        self.regularization = 100.0
        self.classifier = LogisticRegression(C=self.regularization)
        self.beer_data = BeerMLData()
        self.beer_data.from_model()
        self.beer_data.create_beer_mapping()
        self.beer_data.get_mapping_asarray()

    def train(self,pos,neg):

        pos = [self.beer_data.map_beer(beer) for beer in pos]
        neg = [self.beer_data.map_beer(beer) for beer in neg]
       

        X = np.vstack((np.array(pos),np.array(neg)))
        y = np.concatenate((np.ones(len(pos)),np.zeros(len(neg))))

        self.classifier.fit(X,y)

    def classify(self,beer_id):
        mapped = self.beer_data.map_beer(beer_id)
        return self.classifier.predict_proba(np.array([mapped]))

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.cm import jet

    beers_i_like = ['samael-s','rumpkin','the-beast','out-of-bounds-stout']
    beers_i_dont = ['joe-s-pils','raja','ipa']

    

    classifier = LRBeerClassifier()
    classifier.train(beers_i_like,beers_i_dont)

    
    Y = classifier.beer_data.project()
    
    plt.figure()
    plt.gca().set_axis_bgcolor('k')

    for i,beer in enumerate(classifier.beer_data):
        k = beer['name']
        val = classifier.classify(beer['id'])[0][1]
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

