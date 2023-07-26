#Lecture de la température affichée sur la page html avec python
import requests
import re

url = "http://192.168.0.2/"

response = requests.get(url)
html_content = response.text

# Extracting the temperature value using regular expressions
temperature_regex = r"La temperature est de ([\d.]+) degres"
match = re.search(temperature_regex, html_content)
if match:
temperature = match.group(1)
else:
temperature = "N/A" # If no temperature value found

# Displaying the temperature value
print("La température est de", temperature, "degrés.")