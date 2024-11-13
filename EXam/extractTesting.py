import requests
from bs4 import BeautifulSoup
import pandas as pd

# Wikipedia URL for clothing brands
url = 'https://nl.wikipedia.org/wiki/Categorie:Kledingmerk'

# Send a GET request to fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract brand names
brands = []
# Find all the links to brand names within the specific section
for item in soup.select('.mw-category li a'):
    brands.append(item.get_text())

# Convert to a DataFrame
df = pd.DataFrame(brands, columns=['Brand Name'])

# Save the extracted brand names to an Excel file
df.to_excel('tostikaas.xlsx', index=False)

print("Clothing brands have been saved to 'tostikaas.xlsx'")
