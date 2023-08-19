import requests
from bs4 import BeautifulSoup


paginaweb=input("Ingrese el link de la pagina a realizar scraping:")
# URL of the web page you want to scrape
url = paginaweb

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find and print specific elements from the page
    # Example: Extract and print all the links
    links = soup.find_all("a")
    for link in links:
        print(link.get("href"))
else:
    print("Failed to retrieve the webpage")