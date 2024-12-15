from flask import Flask, render_template, request
import requests
import requests.exceptions as err
from datetime import datetime


app = Flask(__name__)

@app.route("/covid",methods =["GET","POST"])
def covidPage():
    data = {}
    if request.method == "POST":
        # response = requests.get("http://api.covid19api.com/summary", verify=False).json()
        # response = requests.get("https://data.covid19india.org/v4/min/data.min.json", verify=False).json()
        try:
            response = requests.get("https://api.rootnet.in/covid19-in/stats/latest", verify=False)
        except (err.HTTPError, err.InvalidJSONError, err.InvalidProxyURL, err.ConnectionError, err.JSONDecodeError, err.RequestsWarning) as error:
            print("Getting Exception as: ", error)
        user_in = (request.form["user_in"]).lower()
        if response.status_code == 200:
            response = response.json()
            information = response['data']['regional']
            for i in range(len(information)):
                if (information[i]['loc']).lower() == user_in:
                    data = {"Confirmed": information[i]["confirmedCasesIndian"], 
                            "Recovered": information[i]["discharged"], 
                            "Deaths": information[i]["deaths"], 
                            "Cases": information[i]["totalConfirmed"], 
                            "status": 200}
                    break
        else:
            data = {"status": 404}
        if data == {}:
            data = {"status": 405}
    return render_template("covid.html", data=data)



@app.route("/weather",methods =["GET","POST"])
def weatherPage():
    data = {}
    if request.method == "POST":
        city = request.form["city"]
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=368f4df90760dcbe671796e6ff7b6eb7"
        response = requests.get(url, verify=False).json()
        # print(response)
        if response["cod"] == 200:
            data = {"City": response["name"], 
                    "Weather": (response["weather"][0]["description"]).title(), 
                    "Weather_code": f"{response['weather'][0]['id']}.jpg",
                    "Temperature_now": round(response["main"]["temp"]-273, 2), 
                    "Visibility": response["visibility"],
                    "Humidity": response["main"]["humidity"], 
                    "Wind_speed": response["wind"]["speed"],
                    "status": 200}
        else:
            data = {"status": 404}
    return render_template("weather.html", data=data)

@app.route("/")
def homePage():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True,port=5000)
