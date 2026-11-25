"""Graphical Weather App using Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox

from weather_service import WeatherError, get_current_weather, get_five_day_forecast


BG = "#eef4fb"
NAVY = "#12345a"
BLUE = "#2475c7"
WHITE = "#ffffff"
MUTED = "#62758b"


class WeatherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("WeatherNow | Live Weather")
        self.root.geometry("790x650")
        self.root.minsize(700, 580)
        self.root.configure(bg=BG)
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg=NAVY, padx=28, pady=22)
        header.pack(fill="x")
        tk.Label(header, text="☀  WeatherNow", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(header, text="Live weather and 5-day forecast powered by OpenWeather",
                 bg=NAVY, fg="#d6e6f7", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        search = tk.Frame(self.root, bg=BG, padx=28, pady=20)
        search.pack(fill="x")
        tk.Label(search, text="Enter city name", bg=BG, fg=NAVY,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        line = tk.Frame(search, bg=BG)
        line.pack(fill="x", pady=(7, 0))
        self.city_entry = ttk.Entry(line, font=("Segoe UI", 12))
        self.city_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.city_entry.insert(0, "Coimbatore")
        ttk.Button(line, text="Get Weather", command=self.search).pack(side="left", padx=(10, 0), ipady=5)
        self.city_entry.bind("<Return>", lambda _event: self.search())

        self.status = tk.Label(self.root, text="Search for a city to see live conditions.",
                               bg=BG, fg=MUTED, font=("Segoe UI", 9))
        self.status.pack(anchor="w", padx=30)

        self.current_card = tk.Frame(self.root, bg=WHITE, padx=22, pady=18,
                                     highlightthickness=1, highlightbackground="#d9e4ef")
        self.current_card.pack(fill="x", padx=28, pady=(10, 16))
        self.city_label = tk.Label(self.current_card, text="Current weather",
                                   bg=WHITE, fg=NAVY, font=("Segoe UI", 16, "bold"))
        self.city_label.pack(anchor="w")
        self.temp_label = tk.Label(self.current_card, text="--°C",
                                   bg=WHITE, fg=BLUE, font=("Segoe UI", 34, "bold"))
        self.temp_label.pack(anchor="w", pady=(8, 0))
        self.desc_label = tk.Label(self.current_card, text="Search a city to load weather",
                                   bg=WHITE, fg=MUTED, font=("Segoe UI", 11))
        self.desc_label.pack(anchor="w")
        self.details_label = tk.Label(self.current_card, text="Humidity: --   Wind: --   Feels like: --",
                                      bg=WHITE, fg=NAVY, font=("Segoe UI", 10))
        self.details_label.pack(anchor="w", pady=(14, 0))

        forecast_frame = tk.Frame(self.root, bg=BG, padx=28)
        forecast_frame.pack(fill="both", expand=True)
        tk.Label(forecast_frame, text="5-DAY FORECAST", bg=BG, fg=NAVY,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 9))
        columns = ("date", "temperature", "description", "humidity")
        self.table = ttk.Treeview(forecast_frame, columns=columns, show="headings", height=6)
        headings = {"date": "Date", "temperature": "Temperature",
                    "description": "Conditions", "humidity": "Humidity"}
        widths = {"date": 145, "temperature": 125, "description": 300, "humidity": 110}
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=widths[col], anchor="center")
        self.table.pack(fill="x")
        footer = tk.Label(self.root, text="Temperatures are shown in Celsius (°C)  •  Results are cached briefly",
                          bg=BG, fg=MUTED, font=("Segoe UI", 8))
        footer.pack(pady=14)

    def search(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("City required", "Please enter a city name.")
            return
        self.status.config(text="Loading weather data…", fg=BLUE)
        self.root.update_idletasks()
        try:
            current = get_current_weather(city)
            forecast = get_five_day_forecast(city)
        except WeatherError as error:
            self.status.config(text="Could not load weather.", fg="#b42318")
            messagebox.showerror("Weather error", str(error))
            return
        except (KeyError, TypeError, ValueError) as error:
            self.status.config(text="Unexpected response from weather service.", fg="#b42318")
            messagebox.showerror("Data error", f"Could not read the weather response: {error}")
            return

        location = current["city"]
        if current["country"]:
            location += f", {current['country']}"
        self.city_label.config(text=location)
        temp = current["temperature"]
        self.temp_label.config(text=f"{temp:.1f}°C" if isinstance(temp, (int, float)) else "--°C")
        self.desc_label.config(text=current["description"])
        humidity = current["humidity"]
        wind = current["wind_speed"]
        feels = current["feels_like"]
        self.details_label.config(
            text=f"Humidity: {humidity if humidity is not None else '--'}%     "
                 f"Wind: {wind if wind is not None else '--'} m/s     "
                 f"Feels like: {feels if feels is not None else '--'}°C"
        )
        for item in self.table.get_children():
            self.table.delete(item)
        for day in forecast:
            t = day["temperature"]
            self.table.insert("", "end", values=(
                day["date"],
                f"{t:.1f}°C" if isinstance(t, (int, float)) else "--",
                day["description"],
                f"{day['humidity']}%" if day["humidity"] is not None else "--",
            ))
        self.status.config(text=f"Weather updated successfully for {location}.", fg="#16803c")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("Treeview", rowheight=30, font=("Segoe UI", 9))
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
    WeatherApp(root)
    root.mainloop()
