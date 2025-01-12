from flask import Flask, request, jsonify
import until

app = Flask(__name__)

@app.route('/classify_image', methods = ['GET, POST'])
def classify_image():
    image_data =  request.files['image_data']    

    if 'image_data' not in request.files:
        return "No file part", 400
    
    file = request.files['image_data']
    if file.filename == '':
        return "No selected file", 400
    
    # Proceed with file processing
    response = jsonify(until.classify_image(image_data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    


if __name__ == "__main__":
    app.run(debug=True,port=5000)
