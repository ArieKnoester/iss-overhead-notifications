import requests
from datetime import datetime
import smtplib

MY_LAT = 0.0  # Your latitude
MY_LONG = 0.0  # Your longitude
# Integer: Number of hours your timezone shifts from UTC.
# Use a negative number if your timezone is behind UTC.
# Take into account if your timezone still observes Daylight Savings Time.
UTC_TIME_SHIFT = 0
EMAIL_HOST = ""
FROM_ADDR = ""
FROM_ADDR_APP_PASSWORD = ""
TO_ADDR = ""


def iss_is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_data = response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if (
        (iss_latitude - 5 < MY_LAT < iss_latitude + 5)
        and
        (iss_longitude - 5 < MY_LONG < iss_longitude + 5)
    ):
        return True
    else:
        return False


def is_after_sunset():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + UTC_TIME_SHIFT
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + UTC_TIME_SHIFT

    time_now_hour = datetime.now().hour
    # print(f"sunrise: {sunrise_hour}, sunset: {sunset_hour}, hour_now: {time_now_hour}")

    if sunset_hour > time_now_hour > sunrise_hour:
        return False
    else:
        return True


def send_email():
    with smtplib.SMTP(EMAIL_HOST) as connection:
        connection.starttls()
        connection.login(user=FROM_ADDR, password=FROM_ADDR_APP_PASSWORD)
        connection.sendmail(
            from_addr=FROM_ADDR,
            to_addrs=TO_ADDR,
            msg="Subject: International Space Station\r\n"
                "The ISS is overhead! Look for it!"
        )


# TODO: Send email every 60 seconds while True
if iss_is_close() and is_after_sunset():
    send_email()
