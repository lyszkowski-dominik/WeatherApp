from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import requests
import sys

app = Flask(__name__)
Base = declarative_base()


class WeatherCard(Base):
    __tablename__ = 'weathercard'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True, nullable=False)

engine = create_engine('sqlite:///weather.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def addCard(name):
    weathercard = WeatherCard()
    weathercard.name = name
    cards = session.query(WeatherCard).all()
    session.close()
    isInDB = False
    for card in cards:
        if card.name == name:
            print('This city already exists')
            isInDB = True
            session.close()
    if isInDB == False:
        session.add(weathercard)
        session.commit()
        session.close()


def getWeatherInfo(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=a01c39f2c2eab487e738bd5930119d7a&units=metric&lang=pl'.format(
        city_name)
    r = requests.get(url).json()
    req_weather = {'name': r['name'], 'temp': round(r['main']['temp'], 1), 'state': r['weather'][0]['description']}
    return req_weather
@app.route('/')
def index():
    return render_template('index.html')
# don't change the following way to run flask:

def addCardsOnSite():
    all_cards = session.query(WeatherCard).all()
    session.close()
    i = 0
    weather_list = []
    while i < len(all_cards):
        for card in all_cards:
            print(card.name)
            req_weather = getWeatherInfo(card.name)
            weather_list.append(req_weather)
            #ranvar = 'weather{}'.format(i)
            i += 1
        return weather_list


@app.route('/', methods=['POST'])
def add_city():
    if request.method == 'POST':
        request_city = request.form['city_name']
        addCard(request_city)
        weather_list = addCardsOnSite()
        print(weather_list)
        return render_template('index.html', weather_list = weather_list)




if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
