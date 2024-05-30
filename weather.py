import requests
import datetime
import geocoder

class WeatherForecast:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        location, date, weather = parts
                        if location not in self.data:
                            self.data[location] = {}
                        self.data[location][date] = float(weather)
                    else:
                        print(f"Error: Invalid data format in line '{line.strip()}'. Skipping.")
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(self.filename, 'w') as file:
            for location, dates in self.data.items():
                for date, weather in dates.items():
                    file.write(f"{location},{date},{weather}\n")

    def __setitem__(self, key, value):
        location, date = key
        if location not in self.data:
            self.data[location] = {}
        self.data[location][date] = value
        self.save_data()

    def __getitem__(self, key):
        location, date = key
        if location in self.data and date in self.data[location]:
            return self.data[location][date]
        else:
            return None

    def __iter__(self):
        for location, dates in self.data.items():
            for date in dates:
                yield date

    def items(self):
        for location, dates in self.data.items():
            for date, weather in dates.items():
                yield date, weather

def get_latitude_longitude():
    while True:
        location = input("Enter location (city, country) or 'end' to terminate: ")
        if location.lower() == 'end':
            return None, None, None
        g = geocoder.arcgis(location)
        if g.ok:
            latitude, longitude = g.latlng
            return latitude, longitude, location
        else:
            print("Error: Location not found. Please try again.")

def get_weather(latitude, longitude, date):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"
        response = requests.get(url)
        data = response.json()
        precipitation = data['daily']['precipitation_sum'][0]
        return precipitation
    except Exception as e:
        print(f"Error: {e}")
        return -1

def main():
    weather_forecast = WeatherForecast("weather_forecast.txt")

    while True:
        latitude, longitude, location = get_latitude_longitude()
        if latitude is None or longitude is None or location is None:
            break

        date_str = input("Enter date (YYYY-mm-dd format, leave blank for next day) or 'end' to change location: ").strip()
        if date_str.lower() == 'end':
            continue

        if not date_str:
            today = datetime.date.today()
            date = today + datetime.timedelta(days=1)
        else:
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Error: Invalid date format. Please use 'YYYY-mm-dd'.")
                continue

        date_str = date.strftime("%Y-%m-%d")
        print(f"Checking weather for {location} on {date_str}...")

        precipitation = get_weather(latitude, longitude, date_str)
        if precipitation == -1:
            print("I don't know.")
        elif precipitation > 0.0:
            print(f"It will rain in {location}. Precipitation value: {precipitation}")
        else:
            print(f"It will not rain in {location}.")

        weather_forecast[(location, date_str)] = precipitation

if __name__ == "__main__":
    main()
