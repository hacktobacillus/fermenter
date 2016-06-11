import simplejson as json, os
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from kettle.utils import get_beers
import numpy as np

class BeerMLData(list):

    def __init__(self):
        self.proj = None
        self.arr = None
        self.beer_mapping = None
        try:
            self.load()
        except: pass
    important_keys = [
        ('hop_varieties',list),
        ('dry_hop_varieties',list),
        ('malt_varieties',list),
        ('yeast_varieties',list),
        ('descriptors',list),
        ('categories',list),
        ('abv',float),
        ('style',str),
        ('price_per_growler',float)
    ]

    def from_model(self):
        self.extend(get_beers(False))

    def from_file(self,fpath):
        with open(fpath,'r') as fp:
            self.extend(json.load(fp))

    def fields(self):
        return [key for key in self[0]['beer'].keys()]

    def get_mapping_asarray(self):
        num_samples = len(self.beer_mapping)
        self.arr = np.zeros((num_samples,self.fs_dim),dtype=float)
        for i,(k,v) in enumerate(self.beer_mapping.items()):
            self.arr[i] = v
        self.compute_pca()
        return self.arr

    def compute_pca(self):
        self.proj = PCA(n_components=2)
        self.proj.fit(self.arr)

    def project(self):
        return self.proj.transform(self.arr)


    def create_beer_mapping(self): 
        data = {}

        self.feature_space_keys = {}
        for key,dtype in self.important_keys:
            self.feature_space_keys[key] = set()
    
        self.fscales = {}

        # Figure out feature space dimensionality

        self.descriptions = []

        for beer in self:

            for key,dtype in self.important_keys:
                fsk = self.feature_space_keys[key]
                dat = dtype(beer[key])
                if dat == 100:
                    continue
                if dtype != list:
                    dat = set([dat])
                self.feature_space_keys[key] = fsk.union(dat)
            
        self.descriptions = [beer['description'] for beer in self]

        self.count_vect = CountVectorizer(stop_words='english')
        X_train_counts = self.count_vect.fit_transform(self.descriptions)
        
        self.tfidf_transformer = TfidfTransformer()
        self.X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        #print(self.X_train_tfidf[0])
        #print(dir(self.X_train_tfidf[0]))


        self.fs_dim = 0
        for k,v in self.feature_space_keys.items():
            if k in ('abv','price_per_growler'):
                self.fs_dim += 1
                continue
            v = list(v)
            v.sort()
            self.feature_space_keys[k] = v
            self.fs_dim += len(v)
        self.fs_dim += self.X_train_tfidf.shape[1] # For the text description.
    

        #compute floating point scales for continuous data
        for k,dtype in self.important_keys:
            if dtype != float: continue
            mx = max(self.feature_space_keys[k])
            self.fscales[k] = mx
        # Map each beer into the binary feature space.
        num_beers = len(self)
       

        self.beer_mapping = {}
        for beer in self:
            #beer = x['beer']
            beer_id = beer['id']
            self.beer_mapping[beer_id] = self.map_beer(beer)

    def get_beer_by_id(self,beer_id):
        beers = [beer for beer in self if beer['id'] == beer_id]
        return beers[0]

    def map_beer(self,x):
        if isinstance(x,str):
            beer = self.get_beer_by_id(x)
        else:
            beer = x
        record = np.zeros(self.fs_dim)
        idx = 0
        for key,dtype in self.important_keys:
            beer_vals = beer[key]

            fsk = self.feature_space_keys[key]

            if dtype == list:
                for k in fsk:
                    qual = k in beer_vals
                    if qual:
                        record[idx] = 1
                    idx += 1
            elif dtype == str:
                for k in fsk:
                    qual = k == beer_vals
                    if qual:
                        record[idx] = 1
                    idx += 1
 
            # divide by their scales...
            else:   
                record[idx] = min(dtype(beer_vals) / self.fscales[key],1.0)
                idx += 1    

        cv = self.count_vect.transform([beer['description']])
        cv = self.tfidf_transformer.transform(cv).todense()
        #print( cv)
        
        


        record[idx:] = cv

        return record


if __name__ == "__main__":
    path = os.path.expanduser('~/Downloads/beer_data.json')

    data = BeerMLData()
    data.from_model()
    #data.from_file(path)
    data.create_beer_mapping()

    X = data.get_mapping_asarray()
    Y = data.project()
    print (data.feature_space_keys['descriptors'])
    print (data.feature_space_keys['categories'])


    import matplotlib
    #matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(X)
    plt.figure()
    plt.gca().set_axis_bgcolor('k')
    plt.plot(Y[:,0],Y[:,1],'ro')
    mapping = data.beer_mapping
    for i,(k,v) in enumerate(mapping.items()):
        plt.text(Y[i,0],Y[i,1],k,color='w')

    plt.show()
    #print(data.fields())
    #print(data[0])
