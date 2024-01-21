import requests
from datetime import datetime
import time
import smtplib
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

my_email = "my@gmail.com"
password = "password"
your_add = "youremail@gmail.com"
def isoverhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT + 5 <= iss_latitude <= MY_LAT - 5 and MY_LONG + 5 <= iss_longitude <= MY_LONG - 5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if isoverhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com",587) as connecton:
            connecton.starttls()
            connecton.login(user=my_email,password=password)
            connecton.sendmail(from_addr=my_email,
                                to_addrs=your_add,
                                msg="Subject: Look up \n\n See ISS is overhead")



