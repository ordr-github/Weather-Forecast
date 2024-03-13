import requests
import tkinter as tk
from tkinter import messagebox

def get_weather(city, api_key):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": city,
        "days": 7,  # Fetch weather for the next 7 days
        "aqi": "yes",  # Air quality index
        "alerts": "yes"  # Weather alerts
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            display_weather_forecast(weather_data)
        elif response.status_code == 400:
            messagebox.showerror("Error",f"There is no city with name {city}. Make sure the spelling is correct.")
        else:
            messagebox.showerror("Error", f"Failed to fetch weather data. Status Code: {response.status_code}\n{response.content}")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Request Exception: {e}")

def display_weather_forecast(weather_data):
    root = tk.Tk()
    root.title("7-Day Weather Forecast")

    
    frame = tk.Frame(root) # Frame for better organization
    frame.pack(padx=20, pady=10)

    # Headers for columns
    tk.Label(frame, text="DATE", font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=10, pady=7, sticky="w")
    tk.Label(frame, text="AVG TEMP(°C)", font=("Helvetica", 14, "bold")).grid(row=0, column=1, padx=10, pady=7, sticky="w")
    tk.Label(frame, text="CONDITION", font=("Helvetica", 14, "bold")).grid(row=0, column=2, padx=10, pady=7, sticky="w")

    for idx, forecast in enumerate(weather_data['forecast']['forecastday'], start=1):
        date_label = tk.Label(frame, text=f"{forecast['date']}", font=("Helvetica", 12))
        date_label.grid(row=idx, column=0, padx=10, pady=7, sticky="w")

        temp_label = tk.Label(frame, text=f"{forecast['day']['avgtemp_c']}°C", font=("Helvetica", 12))
        temp_label.grid(row=idx, column=1, padx=10, pady=7, sticky="w")

        desc_label = tk.Label(frame, text=f"{forecast['day']['condition']['text']}", font=("Helvetica", 12))
        desc_label.grid(row=idx, column=2, padx=10, pady=7, sticky="w")

    root.mainloop()

if __name__ == "__main__":
    api_key = "42650a1b397d4862a8f131417231412"  # WeatherAPI api key
    
    root = tk.Tk() # Create GUI for user input
    root.title("Weather Forecast App")

    root.geometry("300x300")  #Initial window size

    
    city_label = tk.Label(root, text="Enter city name: ", font=("Helvetica", 14)) # Create a label and entry for city input
    city_label.pack(pady=30)

    city_entry = tk.Entry(root, font=("Helvetica", 12))
    city_entry.pack()

    def get_weather_forecast():
        city = city_entry.get()
        if city:
            get_weather(city, api_key)
        else:
            messagebox.showwarning("Warning", "Please enter a city name")

    get_weather_button = tk.Button(root, text="Get Weather Forecast", command=get_weather_forecast, font=("Helvetica", 12))
    get_weather_button.pack(pady=30)

    root.bind('<Return>', lambda event=None: get_weather_forecast()) # Bind the <Return> key event to the get_weather_forecast function

    root.mainloop()
