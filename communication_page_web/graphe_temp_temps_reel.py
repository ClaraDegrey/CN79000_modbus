import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import requests
import re

url = "http://192.168.0.2/"
temperature_history = []
acquisition_active = False

def fetch_temperature():
    response = requests.get(url)
    html_content = response.text

    temperature_regex = r"La temperature est de ([\d.]+) degres"
    match = re.search(temperature_regex, html_content)
    if match:
        return float(match.group(1))
    else:
        return None

def update_temperature(frame):
    temperature = fetch_temperature()
    if temperature is not None:
        temperature_history.append(temperature)
        if len(temperature_history) > 100:
            temperature_history.pop(0)
    line.set_data(range(len(temperature_history)), temperature_history)

    # Update the temperature axis limits
    ax.relim()
    ax.autoscale()

    # Update the current temperature text
    current_temp_text.set_text(f"Température actuelle: {temperature:.2f} °C")

    return line, current_temp_text

def start_acquisition(event):
    global acquisition_active
    acquisition_active = True

def end_acquisition(event):
    global acquisition_active
    acquisition_active = False

    # Prompt user for file location and name
    file_path = input("Enter file location and name: ")
    if file_path:
        # Save temperature data to file
        with open(file_path, "w") as file:
            for i, temperature in enumerate(temperature_history):
                file.write(f"{i}, {temperature}\n")

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot([], [], 'b-')

# Configure the plot
ax.set_xlim(0, 100)  # Set the x-axis limits
ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Real-time Temperature Graph")

# Create a text object for displaying current temperature
current_temp_text = ax.text(0.5, 0.95, "", transform=ax.transAxes,
                            ha="center", va="top")

# Start the real-time temperature update
ani = FuncAnimation(fig, update_temperature, interval=1000, blit=True)

# Create the acquisition control buttons
start_button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
start_button = Button(start_button_ax, "Début d'acquisition")
start_button.on_clicked(start_acquisition)

end_button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
end_button = Button(end_button_ax, "Fin d'acquisition")
end_button.on_clicked(end_acquisition)

# Show the plot
plt.show()

