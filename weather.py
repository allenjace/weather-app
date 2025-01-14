import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage, Canvas
from PIL import Image, ImageTk
import requests
import os
import textwrap
from dotenv import load_dotenv
import sv_ttk

# load api key
load_dotenv() 

# Initialize weather variables
temperature = None
feels_like = None
temp_min = None
temp_max = None
wind = None
pressure = None
humidity = None
weather = None
units = None

# Initialize comparison variables
temperature_city_one = None
feels_like_city_one = None
temp_min_city_one = None
temp_max_city_one = None
wind_city_one = None
pressure_city_one = None
humidity_city_one = None
weather_city_one = None
units_city_one = None

temperature_city_two = None
feels_like_city_two = None
temp_min_city_two = None
temp_max_city_two = None
wind_city_two = None
pressure_city_two = None
humidity_city_two = None
weather_city_two = None
units_city_two = None

# create window for the gui
window = tk.Tk()
window.geometry("1280x720")
window.title("Weather App Gui")
window.resizable(height=None, width=None)

# background mode
current_mode = "dark"
sv_ttk.set_theme(current_mode)

# load bg image
bg_path = Image.open("weather.jpg")
bg = ImageTk.PhotoImage(bg_path)

# Create notebook for multiple pages
notebook = ttk.Notebook(window)
notebook.pack(pady=10, expand=True, fill="both")

# Create main page
main_page = ttk.Frame(notebook)
comparison_page = ttk.Frame(notebook)
settings_page = ttk.Frame(notebook)

# Add pages to notebook
notebook.add(main_page, text="Weather")
notebook.add(comparison_page, text = "Compare Weather")
notebook.add(settings_page, text="Settings")

# create canvas for bg
#canvas1 = Canvas(main_page, width = 500, height = 500)
#canvas1.pack(fill = "both", expand = True)
#canvas1.create_image(0, 0, anchor= "nw", image = bg)

# Main Page Content
weather_title = ttk.Label(main_page, text="Weather App", font=("Hack", 25))
weather_title.pack(pady=10)

city_label = ttk.Label(main_page, text="City:")
city_label.pack(pady=10)
city_entry = ttk.Entry(main_page)
city_entry.pack(pady=10)

temp_units_label = ttk.Label(main_page, text ="Celsius or Fahrenheit?")
temp_units_label.pack()
temp_units = ttk.Combobox(
    main_page,
    state = "readonly",
    values = ["Celsius", "Fahrenheit"]
)
temp_units.pack(pady=10)

def get_units(event):
    value = temp_units.get()
    if value == "Celsius":
        unit_temp = temperature
        unit_feels_like = feels_like
        unit_temp_min = temp_min
        unit_temp_max = temp_max
        unit_wind = wind
        units = "°C"
        
    else:
        unit_temp = (temperature * 9/5) + 32
        unit_feels_like = (feels_like * 9/5) + 32
        unit_temp_min = (temp_min * 9/5) + 32
        unit_temp_max = (temp_max * 9/5) + 32
        unit_wind = wind * 2.237
        units = "°F"
        
    display_weather.config(text=f"Temperature: {unit_temp:.0f}{units}\n\n"
                               f"Feels Like: {unit_feels_like:.0f}{units}\n\n"
                               f"Temp Min: {unit_temp_min:.0f}{units}\n\n"
                               f"Temp Max: {unit_temp_max:.0f}{units}\n\n"
                               f"Wind: {unit_wind:.0f} m/s\n\n" 
                               f"Pressure: {pressure:.0f} hPa (hectopascals)\n\n"
                               f"Humidity: {humidity:.0f}%\n\n"
                               f"Weather: {weather.capitalize()}", 
                               font=("Hack", 12))

weather_data = ttk.Button(main_page, text="Get the Weather")
weather_data.pack(pady=10)

display_weather = ttk.Label(main_page, text="")
display_weather.pack(pady=10)

# Define the function to fetch weather data
def fetch_weather():
    global temperature, feels_like, temp_min, temp_max, wind, pressure, humidity, weather, units

    city = city_entry.get()
    # Add your API key here
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        messagebox.showerror("Error", "API key not found!")
        return
        
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, api_key)

    try:
        response = requests.get(url)
        data = response.json()
        
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        wind = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        
        get_units(None)
        
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

weather_data.config(command=fetch_weather)

class Comparison:
    
    comparison_title = ttk.Label(comparison_page, text="Compare the weathers of two cities! ", font=("Hack", 20))
    comparison_title.pack(pady=20)
    
    city_one = ttk.Label(comparison_page, text = "City One:", font=("Hack", 15))
    city_one.pack(pady = 10)
    city_one_btn = ttk.Entry(comparison_page)
    city_one_btn.pack(pady = 20)
    
    
    city_two = ttk.Label(comparison_page, text = "City Two:", font=("Hack", 15))
    city_two.pack(pady = 10)
    city_two_btn = ttk.Entry(comparison_page)
    city_two_btn.pack(pady = 20)
    
    temp_units_label = ttk.Label(comparison_page, text ="Celsius or Fahrenheit?" , font=("Hack", 15))
    temp_units_label.pack()
    temp_units = ttk.Combobox(
        comparison_page,
        state = "readonly",
        values = ["Celsius", "Fahrenheit"]
    )
    temp_units.pack(pady=20)
    
    compare_btn = ttk.Button(comparison_page, text="Compare")
    compare_btn.pack(pady = 10)
    
    display_weather = ttk.Label(comparison_page, text="")
    display_weather.pack(pady=10, padx = 20)
    
    @staticmethod
    def get_units(event):
        value = Comparison.temp_units.get()
        if temperature_city_one is not None and temperature_city_two is not None:
            city_one = Comparison.city_one_btn.get()
            city_two = Comparison.city_two_btn.get()
            if value == "Celsius":
                unit_temp_city_one = temperature_city_one
                unit_feels_like_city_one = feels_like_city_one
                unit_temp_min_city_one = temp_min_city_one
                unit_temp_max_city_one = temp_max_city_one
                unit_wind_unit_one = wind_city_one
                units_city_one = "°C"
                
                unit_temp_city_two = temperature_city_two
                unit_feels_like_city_two = feels_like_city_two
                unit_temp_min_city_two = temp_min_city_two
                unit_temp_max_city_two = temp_max_city_two
                unit_wind_unit_two = wind_city_two
                units_city_two = "°C"
                
            else:
                unit_temp_city_one = (temperature_city_one * 9/5) + 32
                unit_feels_like_city_one = (feels_like_city_one * 9/5) + 32
                unit_temp_min_city_one = (temp_min_city_one * 9/5) + 32
                unit_temp_max_city_one = (temp_max_city_one * 9/5) + 32
                unit_wind_unit_one = wind_city_one * 2.237
                units_city_one = "°F"
                
                unit_temp_city_two = (temperature_city_two * 9/5) + 32
                unit_feels_like_city_two = (feels_like_city_two * 9/5) + 32
                unit_temp_min_city_two = (temp_min_city_two * 9/5) + 32
                unit_temp_max_city_two = (temp_max_city_two * 9/5) + 32
                unit_wind_unit_two = wind_city_two * 2.237
                units_city_two = "°F"
                
            city_one_text= (
                f"City One: {city_one}\n\n"
                f"Temperature: {unit_temp_city_one:.0f}{units_city_one}\n\n"
                f"Feels Like: {unit_feels_like_city_one:.0f}{units_city_one}\n\n"
                f"Temp Min: {unit_temp_min_city_one:.0f}{units_city_one}\n\n"
                f"Temp Max: {unit_temp_max_city_one:.0f}{units_city_one}\n\n"
                f"Wind: {unit_wind_unit_one:.0f} m/s\n\n" 
                f"Pressure: {pressure_city_one:.0f} hPa (hectopascals)\n\n"
                f"Humidity: {humidity_city_one:.0f}%\n\n"
                f"Weather: {weather_city_one.capitalize()}\n\n"
            )
                                    
            city_two_text = (
                f"City Two: {city_two}\n\n"
                f"Temperature: {unit_temp_city_two:.0f}{units_city_two}\n\n"
                f"Feels Like: {unit_feels_like_city_two:.0f}{units_city_two}\n\n"
                f"Temp Min: {unit_temp_min_city_two:.0f}{units_city_two}\n\n"
                f"Temp Max: {unit_temp_max_city_two:.0f}{units_city_two}\n\n"
                f"Wind: {unit_wind_unit_two:.0f} m/s\n\n" 
                f"Pressure: {pressure_city_two:.0f} hPa (hectopascals)\n\n"
                f"Humidity: {humidity_city_two:.0f}%\n\n"
                f"Weather: {weather_city_two.capitalize()}"
            )
    
            # wrap to columns
            city_one_wrapped = textwrap.fill(city_one_text, width = 40)
            city_two_wrapped = textwrap.fill(city_two_text, width = 40)
            
            # Combine both paragraphs for display
            comparison_text = f"{city_one_wrapped}\n\n{'='*40}\n\n{city_two_wrapped}"
            
            # Print the paragraphs side-by-side
            Comparison.display_weather.config(text = comparison_text)
    
    # Define the function to fetch weather data
    @staticmethod
    def fetch_weather():
        global temperature_city_one, feels_like_city_one, temp_min_city_one, temp_max_city_one, wind_city_one, pressure_city_one, humidity_city_one, weather_city_one, units_city_one
        global temperature_city_two, feels_like_city_two, temp_min_city_two, temp_max_city_two, wind_city_two, pressure_city_two, humidity_city_two, weather_city_two, units_city_two

        city_one = Comparison.city_one_btn.get()
        city_two = Comparison.city_two_btn.get()
        # Add your API key here
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            messagebox.showerror("Error", "API key not found!")
            return
            
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'

        try:
            response_city_one = requests.get(url.format(city_one, api_key))
            data_city_one = response_city_one.json()
            
            temperature_city_one = data_city_one["main"]["temp"]
            feels_like_city_one = data_city_one["main"]["feels_like"]
            temp_min_city_one = data_city_one["main"]["temp_min"]
            temp_max_city_one = data_city_one["main"]["temp_max"]
            wind_city_one = data_city_one["wind"]["speed"]
            pressure_city_one = data_city_one["main"]["pressure"]
            humidity_city_one = data_city_one["main"]["humidity"]
            weather_city_one = data_city_one["weather"][0]["description"]
            
            response_city_two = requests.get(url.format(city_two, api_key))
            data_city_two = response_city_two.json()
            
            temperature_city_two = data_city_two["main"]["temp"]
            feels_like_city_two = data_city_two["main"]["feels_like"]
            temp_min_city_two = data_city_two["main"]["temp_min"]
            temp_max_city_two = data_city_two["main"]["temp_max"]
            wind_city_two = data_city_two["wind"]["speed"]
            pressure_city_two = data_city_two["main"]["pressure"]
            humidity_city_two = data_city_two["main"]["humidity"]
            weather_city_two = data_city_two["weather"][0]["description"]
            
            Comparison.get_units(None)
            
        except Exception as e:
            messagebox.showerror("Error", "Unable to fetch weather data")

    compare_btn.config(command = fetch_weather)
    
Comparison.temp_units.bind('<<ComboboxSelected>>', Comparison.get_units)


# Settings Page Content
class Settings:
    @staticmethod
    def toggle_modes():
        global current_mode
        if current_mode == "dark":
            sv_ttk.set_theme("light")
            current_mode = "light"
            mode_label.config(text="Current Mode: Light")
        else:
            sv_ttk.set_theme("dark")
            current_mode = "dark"
            mode_label.config(text="Current Mode: Dark")

# Settings page layout
settings_title = ttk.Label(settings_page, text="Settings", font=("Hack", 25))
settings_title.pack(pady=20)

mode_label = ttk.Label(settings_page, text="Current Mode: Dark")
mode_label.pack(pady=10)

toggle_button = ttk.Button(settings_page, text="Toggle Theme", command=Settings.toggle_modes)
toggle_button.pack(pady=10)

# main loop for the window
window.mainloop()