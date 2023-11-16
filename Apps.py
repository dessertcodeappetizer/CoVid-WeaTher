from flask import Flask, render_template, request
import requests
from datetime import datetime


app = Flask(__name__)

@app.route("/covid",methods =["GET","POST"])
def covidPage():
    data = {}
    if request.method == "POST":
        # response = requests.get("http://api.covid19api.com/summary", verify=False).json()
        response = requests.get("https://data.covid19india.org/v4/min/data.min.json", verify=False).json()
        user_in = request.form["user_in"]
        
        try:
            state_list = response[user_in]
            information = state_list["total"]
            data = {
                "Confirmed": information["confirmed"], "Deceased": information["deceased"], "Recovered": information["recovered"], 
                "Tested": information["tested"], "Vaccinated1": information["vaccinated1"], 
                "Vaccinated2": information["vaccinated2"], "status": 200
            }
        except KeyError:
            data = {"status": 404}
        
        
    return render_template("covid.html", data = data)




@app.route("/weather",methods =["GET","POST"])
def weatherPage():
    data = {}
    if request.method == "POST":
        city = request.form["city"]
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=368f4df90760dcbe671796e6ff7b6eb7"
        response = requests.get(url, verify=False).json()
        # print(response)
        if response["cod"] == 200:
            data = {"City": response["name"], "Latitude": response["coord"]["lat"], "Longitude":response["coord"]["lon"], "Sunrise": datetime.fromtimestamp(response["sys"]["sunrise"]), "Sunset": datetime.fromtimestamp(response["sys"]["sunset"]), "Temperature": round(response["main"]["temp_max"]-273,2), "Humidity": response["main"]["humidity"], "status": 200}
        else:
            data = {"status": 404}
    return render_template("weather.html", data=data)

@app.route("/")
def homePage():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True,port=5000)







