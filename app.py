from flask import Flask
from flask import render_template
from flask import request
import requests
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
# don't change the following way to run flask:

@app.route('/add', methods=['POST'])
def add_city():
    if request.method == 'POST':
        request_city = request.form['city_name']
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=6476e9515765d4437dc65184cdf34309&units=metric&lang=pl'.format(request_city)
        r = requests.get(url).json()
        print(r)
        req_weather = {'name': r['name'] , 'temp': round(r['main']['temp'],1), 'state': r['weather'][0]['description']}
    return render_template('index.html', weather=req_weather)





if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
