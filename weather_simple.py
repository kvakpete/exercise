import requests
import datetime
import geocoder

def get_latitude_longitude():
    while True:
        location = input("Enter location (city, country): ")
        g = geocoder.arcgis(location)
        if g.ok:
            latitude, longitude = g.latlng
            return latitude, longitude, location
        else:
            print("Error: Location not found. Please try again.")

def get_weather(latitude, longitude, date):
    try:
        # Construct the API URL with the latitude, longitude, and searched date
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"

        # Make a request to the API
        response = requests.get(url)
        data = response.json()

        # Extract precipitation data
        precipitation = data['daily']['precipitation_sum'][0]

        return precipitation
    except Exception as e:
        print(f"Error: {e}")
        return -1

def main():
    # latitude, longitude, and location for the specified location
    latitude, longitude, location = get_latitude_longitude()

    # ask the user for a date
    date_str = input("Enter date (YYYY-mm-dd format, leave blank for next day): ").strip()

    # If no date is provided, next day
    if not date_str:
        today = datetime.date.today()
        date = today + datetime.timedelta(days=1)
    else:
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date format. Please use 'YYYY-mm-dd'.")
            return

    date_str = date.strftime("%Y-%m-%d")
    print(f"Checking weather for {location} on {date_str}...")

    # Get the weather status for the specified location and date
    precipitation = get_weather(latitude, longitude, date_str)
    if precipitation == -1:
        print("I don't know.")
    elif precipitation > 0.0:
        print(f"It will rain in {location}. Precipitation value: {precipitation}")
    else:
        print(f"It will not rain in {location}.")

if __name__ == "__main__":
    main()
