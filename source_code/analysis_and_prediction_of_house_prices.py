#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:08:45 2024

@author: aashi
"""
import io
import pickle
from flask import Flask, request, send_file
from flasgger import Swagger
import pandas as pd


#Loading the trained XGBoost model using pickle
with open(r'../analysis_and_prediction_of_house_prices/model_artifacts/xgb.pkl', 'rb') as model_pkl:
    model = pickle.load(model_pkl)


#Loading the saved scaler using pickle
with open(r'../analysis_and_prediction_of_house_prices/model_artifacts/sc.pkl', 'rb') as sc_pkl:
    sc = pickle.load(sc_pkl)
  
    
app = Flask(__name__)
swagger = Swagger(app)


#Defining function to create a new column - BedroomRatio
def calculate_bedroom_ratio(dataset):
    dataset['BedroomRatio'] = dataset['AveBedrms'] / dataset['AveRooms']
    return dataset


#Defining function to rearrange specific columns
def rearrange_columns(dataset):
    # Define the columns you want to keep and rearrange
    expected_columns = ['MedInc','HouseAge','AveRooms','AveBedrms','Population','AveOccup','Latitude','Longitude','BedroomRatio']
    # Select only the available columns in the dataset
    dataset = dataset[[col for col in expected_columns if col in dataset.columns]]
    return dataset


# Defining API endpoint to handle file upload
@app.route('/predict', methods=['POST'])
def predict():
    """
    This is the prediction endpoint.
    It takes a CSV file as input and returns predictions.
    ---
    parameters:
      - name: input_file
        in: formData
        type: file
        required: true
        description: The CSV file containing the input data.
    responses:
      200:
        description: Predictions of Property Valuation
    """
    #reading the input file
    input_data = pd.read_csv(request.files.get("input_file"))
    
    #retaining the original input data
    original_input_data = input_data
    
    #creating new column i.e. feature engineering
    input_data = calculate_bedroom_ratio(input_data)
    
    #rearraging columns to match expected order for model consumption
    input_data = rearrange_columns(input_data)
    
    
    #standardizing numerical variables using saved scaler
    input_data = sc.transform(input_data)
    
    #performing predictions using the pre-trained model
    predictions = model.predict(input_data)
    
    #appending predictions to the original input data
    original_input_data['Predictions_MedHouseVal'] = predictions
    

    #creating an in-memory CSV file with both input data and predictions
    output = io.BytesIO()
    original_input_data.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)

    #sending the CSV file as a response
    return send_file(output, mimetype='text/csv', as_attachment=True, attachment_filename='predictions_output.csv')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)