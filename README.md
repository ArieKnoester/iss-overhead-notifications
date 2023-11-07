# iss-overhead-notifications

Work in progress.

A small Python course exercise working with APIs. Data is retrieved
from Open Notify: International Space Station Current Location
(http://open-notify.org/Open-Notify-API/ISS-Location-Now/) and 
Sunrise Sunset (https://sunrise-sunset.org/api) APIs.

If the International Space Station is close to your location
(within plus or minus 5 latitude and longitude) and it is after 
sunset, this program sends an email notification, so you can attempt
to look for it in the night sky.

### Note: For this program to work
- Constant variables must be filled in.
- It would be best to create a bash script and 
schedule it to run this code at regular intervals.