"""Command-line version of the WeatherNow application."""
from weather_service import WeatherError, get_current_weather, get_five_day_forecast


def main():
    print("=" * 52)
    print("             WEATHER NOW - LIVE WEATHER")
    print("=" * 52)
    while True:
        city = input("\nEnter city name (blank to quit): ").strip()
        if not city:
            print("Thank you for using WeatherNow. Goodbye!")
            break
        try:
            current = get_current_weather(city)
            forecast = get_five_day_forecast(city)
            place = current["city"]
            if current["country"]:
                place += f", {current['country']}"
            print(f"\nCURRENT WEATHER: {place}")
            print("-" * 52)
            print(f"Temperature : {current['temperature']} °C")
            print(f"Feels like  : {current['feels_like']} °C")
            print(f"Humidity    : {current['humidity']}%")
            print(f"Conditions  : {current['description']}")
            print(f"Wind speed  : {current['wind_speed']} m/s")
            print("\n5-DAY FORECAST")
            print("-" * 70)
            print(f"{'DATE':<14} {'TEMP':<12} {'CONDITIONS':<28} {'HUMIDITY'}")
            for day in forecast:
                print(f"{day['date']:<14} {str(day['temperature']) + ' °C':<12} "
                      f"{day['description']:<28} {str(day['humidity']) + '%'}")
        except WeatherError as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
