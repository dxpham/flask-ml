from flask import Flask, request, jsonify, render_template
from flask.logging import create_logger
import logging
import requests
# import mlib

 
from time import strftime
from flask import  flash, request
from wtforms import Form, TextField, FloatField, validators, StringField, SubmitField

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

MODEL_URL="http://localhost:8080/predict/"

class ReusableForm(Form):
    weight = FloatField('Weight:', validators=[validators.required()])
     
def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(weight):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, Weight={}  \n'.format(timestamp, weight))
    data.close()

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    #print(form.errors)
    if request.method == 'POST':
        weight= request.form['weight']
        
        if form.validate():
            write_to_disk(weight)

            prediction = requests.get(MODEL_URL+str(weight))
            prediction = prediction.json()['prediction']            
            flash(f'{prediction["height_inches"]} inches or {prediction["height_human_readable"]} tall for a player who weights {weight} lbs.')

        else:
            flash('Error: Try another time!')

        

    return render_template('index.html', form=form)


# @app.route("/predict", methods=['POST'])
# def predict():
#     """Predicts the Height of MLB Players"""
    
#     json_payload = request.json
#     LOG.info(f"JSON payload: {json_payload}")
#     prediction = mlib.predict(json_payload['Weight'])
#     return jsonify({'prediction': prediction})


if __name__ == "__main__":
    app.run()

 
