import json
import pickle
import numpy as np


__cuisine_type =  None
__data_columns =  None
__model =  None



def load_saved_artifacts () :
    print("loading saved articats..start")

    global __cuisine_type
    global __data_columns
    global __model

    #load cuisine_type
    with open('server/artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __cuisine_type =__data_columns[3:]


    #load model
    with open('server/artifacts/predict_restaurent__monthly_revenue', 'rb') as f:
        __model = pickle.load(f)

    print("loading saved articats..done")

def predict_monthly_revenue(number_of_customers, menu_price, marketing_spend, cuisine_type):
    try:
        type_index = __data_columns.index(cuisine_type.lower())
    except:
        type_index = -1
        
    x = np.zeros(len(__data_columns))
    x[0] = number_of_customers
    x[1] = menu_price
    x[2] = marketing_spend
    
    if type_index > 0 :
        return round(__model.predict([x])[0],2)

def get_cuisine_type():
    return __cuisine_type

def get_data_columns():
    return __data_columns



if __name__== "__main__":
    load_saved_artifacts()
    print(predict_monthly_revenue(58,36.50,4.5,'mexican'))
    print(get_cuisine_type())