from flask import Flask, render_template, redirect, request
import json,requests
from security import safe_requests

app = Flask(__name__)


@app.route("/", methods = ['GET'])
def getLocation():
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = safe_requests.get(geo_request_url)
    geo_data = geo_request.json()
    lat = geo_data['latitude']
    long = geo_data['longitude']
    return redirect("/lat=" + str(lat) + "&long=" + str(long))


@app.route('/lat=<string:lat>&long=<string:long>', methods = ['GET','POST'])
def getWeather(lat, long):
    if(request.method == 'POST'):
        city = request.form['city'];
        return redirect(('/city/' + str(city)))
    else: 
        weather = safe_requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + long + '&units=metric&appid=c1547e16f89f47b9711cb39aa31ce3a9');
        weatherData = json.loads(weather.text);
        temp = str(weatherData['main']['temp']);
        cityname = str(weatherData['name'])
        img = "../static/images/" + str(weatherData['weather'][0]['icon']) + ".png"
        return render_template("index.html", temp = temp, src = img, name = cityname);
    
@app.route('/city/<string:cityname>')
def getWeatherByCity(cityname):
    weatherByCity = safe_requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + str(cityname) + '&units=metric&appid=c1547e16f89f47b9711cb39aa31ce3a9')
    weatherData = json.loads(weatherByCity.text)
    temp = str(weatherData['main']['temp'])
    img = "../static/images/" + str(weatherData['weather'][0]['icon']) +".png"
    mintemp = str(weatherData['main']['temp_min'])
    maxtemp = str(weatherData['main']['temp_max'])
    desc = str(weatherData['weather'][0]['main'])
    feels = str(weatherData['main']['feels_like'])
    citynameByAPI = str(weatherData['name'])
    humidity = str(weatherData['main']['humidity'])
    return render_template('city.html', temp = temp, src = img, mintemp = mintemp, maxtemp  = maxtemp, desc = desc, feels = feels, name = citynameByAPI, humidity = humidity)

@app.route('/about')
def aboutMe():
    return render_template('about.html')
if(__name__ == '__main__'):
    app.run(debug=True)
