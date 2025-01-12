from flask import Flask, request, jsonify

import utils

app = Flask(__name__)

@app.route('/get_cuisine_type', methods = ['GET'])  

def get_cuisine_type():
    response = jsonify({
        'cuisine_Type' : utils.get_cuisine_type()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_monthly_revenue', methods = ['POST'])
def predict_monthly_revenue():
    try:
        number_of_customers = int(request.form['number_of_customers'])
        menu_price = float(request.form['menu_price'])
        marketing_spend = float(request.form['marketing_spend'])
        cuisine_type = request.form['cuisine_type']

        estimated_revenue = utils.predict_monthly_revenue(number_of_customers, menu_price, marketing_spend, cuisine_type)
        response = jsonify({ "estimated_revenue" : estimated_revenue})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except ValueError as e:
        return jsonify({'error': 'Invalid input'})
    except Exception as e:  
        return jsonify({'error': 'An error occurred'})
    


if __name__== "__main__":
    print("Python Flask Has Been Strated For Revenue Prediction")
    utils.load_saved_artifacts()
    app.run()
    