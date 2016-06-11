import simplejson as json, os
import numpy as np

class BeerMLData(list):

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
        pass
    def from_file(self,fpath):
        with open(fpath,'r') as fp:
            self.extend(json.load(fp))

    def fields(self):
        return [key for key in self[0]['beer'].keys()]

    def get_mapping_asarray(self):
        num_samples = len(self.beer_mapping)
        arr = np.zeros((num_samples,self.fs_dim),dtype=float)
        for i,(k,v) in enumerate(self.beer_mapping.items()):
            arr[i] = v
        return arr

    def create_beer_mapping(self): 
        data = {}

        self.feature_space_keys = {}
        for key,dtype in self.important_keys:
            self.feature_space_keys[key] = set()
    
        self.fscales = {}

        # Figure out feature space dimensionality
        for x in self:
            beer = x['beer']
            for key,dtype in self.important_keys:
                fsk = self.feature_space_keys[key]
                dat = dtype(beer[key])
                if dat == 100:
                    continue
                if dtype != list:
                    dat = set([dat])
                self.feature_space_keys[key] = fsk.union(dat)

        self.fs_dim = 0
        for k,v in self.feature_space_keys.items():
            if k in ('abv','price_per_growler'):
                self.fs_dim += 1
                continue
            v = list(v)
            v.sort()
            self.feature_space_keys[k] = v
            self.fs_dim += len(v)

        #compute floating point scales for continuous data
        for k,dtype in self.important_keys:
            if dtype != float: continue
            mx = max(self.feature_space_keys[k])
            self.fscales[k] = mx
        # Map each beer into the binary feature space.
        num_beers = len(self)
       

        self.beer_mapping = {}
        for x in self:
            beer = x['beer']
            beer_id = beer['id']
            self.beer_mapping[beer_id] = self.map_beer(beer)

    def map_beer(self,beer):
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
        return record


if __name__ == "__main__":
    path = os.path.expanduser('~/Downloads/beer_data.json')

    data = BeerMLData()
    data.from_file(path)
    data.create_beer_mapping()

    X = data.get_mapping_asarray()
    import matplotlib
    #matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(X)
    plt.savefig('test.png')
    #print(data.fields())
    #print(data[0])
