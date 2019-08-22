from flask import Flask, render_template, url_for
import requests
from io import StringIO
from random import choice
from random import randint
from decouple import config
import json


app = Flask(__name__)

api_key = config('API_KEY')
rover_url = config('ROVER_URL')
sol = randint(1, 1000)


@app.route("/api")
def get_photo():
    params={'sol':sol, 'api_key':api_key}
    response = requests.get(rover_url, params)
    response_dictionary = response.json()
    photos = response_dictionary['photos']

    return choice(photos)['img_src']

@app.route("/")
def index():
    captured_photo = get_photo()

    return render_template('index.html', photo=captured_photo)

# Number of people in space
@app.route('/peopleInSpace')
def people_in_space():
    response = requests.get('http://api.open-notify.org/astros.json')
    data = response.json()
    return render_template('people_in_space.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)