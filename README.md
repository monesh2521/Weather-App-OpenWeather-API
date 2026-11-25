# WeatherNow – Live Weather App (InternCircle Project 05)

A Python application that retrieves real-time weather and a five-day forecast using the **OpenWeather API**. It includes a Tkinter graphical interface and a command-line version.

## Features

- Current temperature in Celsius, feels-like temperature, humidity, wind speed and weather description
- Five-day forecast table (one representative forecast entry per day)
- REST API calls using `requests` and JSON response parsing
- API key loaded from `.env` (never hard-coded)
- Handles missing keys, unknown cities, invalid API keys, timeouts, network errors and API limits
- Ten-minute in-memory cache to reduce repeated API requests
- GUI and CLI interfaces

## Requirements

- Python 3.9 or newer
- Internet connection
- Free OpenWeather account and API key
- Tkinter (included with most standard Windows Python installations)

## Setup on Windows (VS Code / PowerShell)

1. Extract the ZIP and open the project folder in VS Code.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create an OpenWeather account at https://openweathermap.org/api and obtain an API key.
5. Copy `.env.example` and rename the copy to `.env`.
6. Open `.env` and replace the placeholder:

   ```env
   OPENWEATHER_KEY=your_real_api_key_here
   ```

   Do not add quotation marks. Keep `.env` private. A newly generated key may take some time to activate.

## Run the application

### Graphical interface

```powershell
python app.py
```

Enter a city name and click **Get Weather** (or press Enter).

### Command-line interface

```powershell
python cli.py
```

Enter a city name. Press Enter on a blank input to exit.

## Project structure

```text
InternCircle_Project_05_Weather_App/
├── app.py              # Tkinter graphical interface
├── cli.py              # Command-line interface
├── weather_service.py  # API requests, JSON parsing, caching and errors
├── requirements.txt    # Python dependencies
├── .env.example        # Safe API-key template (copy to .env)
├── .gitignore          # Excludes .env and Python-generated files
└── README.md           # Setup and usage instructions
```

## API endpoints

- Current conditions: `https://api.openweathermap.org/data/2.5/weather`
- Five-day forecast: `https://api.openweathermap.org/data/2.5/forecast`

Requests use `units=metric`, so temperatures are returned in Celsius. Forecast entries are grouped by date and the entry nearest 12:00 is selected for each day.

## API key security

The real key is stored locally in `.env` and read with `python-dotenv`. The `.env` file is listed in `.gitignore`, so it should not be uploaded to GitHub. Only `.env.example` with a placeholder is included in this project. Before pushing, run:

```powershell
git status
```

Confirm that `.env` is not listed.

## Testing checklist

Test at least five cities, for example Coimbatore, Chennai, Bengaluru, London and Tokyo. Also test:
- An invalid city name (should show a city-not-found message)
- An empty city input (GUI warning; blank CLI input exits)
- A missing or invalid API key (clear setup/API-key message)
- A disconnected network (friendly network error)

A successful live result requires your own valid OpenWeather API key and internet connection. Do not submit a fabricated screenshot; capture the running app after a real API response.

## Submission items

1. GitHub repository link containing the source code and README (without `.env`)
2. Screenshot of the app showing a real weather result
3. A short note explaining that the API key is kept in `.env` and excluded using `.gitignore`

## Troubleshooting

- **401 Unauthorized:** verify the key and allow time for a new key to activate.
- **404 Not Found:** check the city spelling.
- **Network error:** check internet access and try again.
- **Tkinter missing:** use the CLI with `python cli.py`, or install the Python distribution that includes Tcl/Tk.
