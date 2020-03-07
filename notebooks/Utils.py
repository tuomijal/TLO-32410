import pandas as pd

def load(name, raw=False):
    data = pd.read_csv(f"http://data.insideairbnb.com/spain/catalonia/barcelona/2020-02-16/data/{name}.csv.gz")

    if raw:
        return data
    

    return data


def clean_listings_detailed(listings_detailed):
    """
    
    """
    price = listings_detailed.price.str[1:].replace("$", '')
    price = price.str.replace(',', '')
    listings_detailed.price = price.astype(float)
    listings_detailed = listings_detailed[listings_detailed.price!=0]
    listings_detailed['price_log'] = np.log(listings_detailed.price)
    
    return listings_detailed