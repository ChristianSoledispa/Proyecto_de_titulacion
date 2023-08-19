import requests
import re

paginaweb=input("Ingrese el link de la pagina a realizar scraping:")
# URL of the web page you want to scrape
url = paginaweb


palabrabuscar=input("Ingrese la palabra a buscar:")
# Word you're looking for
target_word = palabrabuscar

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use regular expressions to count occurrences of the target word
    occurrences = len(re.findall(r'\b' + re.escape(target_word) + r'\b', response.text, re.IGNORECASE))
    
    print(f"The word '{target_word}' was found {occurrences} times on the webpage.")
else:
    print("Failed to retrieve the webpage")