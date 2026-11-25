# Project 05 – Submission Notes

**Project title:** Weather App with Live OpenWeather API  
**Language:** Python  
**Libraries:** requests, python-dotenv, Tkinter  
**API:** OpenWeather Current Weather and 5-Day Forecast

## Project description
This project connects Python to the OpenWeather REST API. It requests current weather and forecast data for a city, parses the JSON response, and displays temperature, humidity, weather conditions and wind speed. The project provides both a Tkinter GUI and a command-line interface.

## Main concepts demonstrated
- REST API integration using `requests.get()`
- Query parameters and JSON response parsing
- Reading nested JSON fields safely
- API-key management using environment variables
- Error handling for unknown cities, invalid keys and network failures
- Short-lived caching to avoid unnecessary repeated requests

## Security note
The API key is stored in a local `.env` file. The `.env` file is ignored by Git through `.gitignore`. Only `.env.example`, which contains a placeholder, is included in the repository.

## Before submitting
- Add your own valid OpenWeather API key to `.env`.
- Run `python app.py` and verify a live result.
- Test at least five cities and an invalid city.
- Capture a genuine screenshot of the running application.
- Confirm `.env` is not tracked with `git status`.
- Upload the source code and README to GitHub, then submit the repository link and screenshot.
