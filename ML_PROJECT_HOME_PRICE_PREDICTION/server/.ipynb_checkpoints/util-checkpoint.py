import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower()) ##get the column index 
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft 
    x[1] = bath 
    x[2] = bhk 

    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def load_saved_artifacts():
    print("loading saved articats..start")
    global __locations
    global __data_columns
    global __model
    #load location
    with open('server/artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    #load model
    with open('server/artifacts/banglore_home_price_prediction', 'rb') as f:
        __model = pickle.load(f)
    print("loading saved articats..done")
    
def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__== "__main__":
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Vishveshwarya Layout', 1000, 2, 2))
    print(get_estimated_price('Vishveshwarya Layout', 1000, 3, 2))
    print(get_estimated_price('Yelenahalli', 1000, 2, 2))
    print(get_estimated_price('Yelenahalli', 1000, 2, 3))