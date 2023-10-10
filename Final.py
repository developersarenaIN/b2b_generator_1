import importlib
import requests
from bs4 import BeautifulSoup
import csv
import time

# Check and install missing modules
def check_and_install_module(module_name):
    try:
        importlib.import_module(module_name)
    except ImportError:
        print(f"Installing {module_name}...")
        import subprocess
        subprocess.check_call(["pip", "install", module_name])
        print(f"{module_name} installed successfully.")

# Check and install required modules
required_modules = ["requests", "bs4", "csv"]
for module in required_modules:
    check_and_install_module(module)

import requests
from bs4 import BeautifulSoup
import csv
import time



def display_loading_message(duration):
    print("𝐁𝟐𝐁 𝐋𝐞𝐚𝐝 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧 𝐓𝐨𝐨𝐥 𝐁𝐲 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫𝐬 𝐀𝐫𝐞𝐧𝐚 - 𝐍𝐎𝐓 𝐅𝐎𝐑 𝐒𝐀𝐋𝐄 \n 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫𝐬 𝐀𝐫𝐞𝐧𝐚 Will not be held liable if this tool is used for illegal or spamming reasons. ")
    print("Loading...", end="", flush=True)
    time.sleep(duration)
    print("\n")

def scrape_yellowpages(keyword, area, num_pages):
    base_url = f"https://www.yellowpages.com/search?search_terms={keyword}&geo_location_terms={area}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    scraped_data = []

    page_num = 1
    while page_num <= num_pages:
        response = requests.get(f"{base_url}&page={page_num}", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        results = soup.find_all("div", class_="result")
        if not results:
            break

        for result in results:
            name = result.find("a", class_="business-name").get_text(strip=True)
            website = result.find("a", class_="track-visit-website")
            website = website["href"] if website else "N/A"
            number = result.find("div", class_="phones").get_text(strip=True)

            # Extract address information
            address = result.find("div", class_="street-address").get_text(strip=True)

            scraped_data.append((name, website, number, address))

        page_num += 1

    return scraped_data

def extract_email_from_website(website):
    return "N/A"

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Name", "Website", "Number", "Address", "Email"])  # Write header row
        csv_writer.writerows(data)

if __name__ == "__main__":
    display_loading_message(3)  # Display the loading message for 3 seconds

    keyword = input("Enter Your Niche/Service(Ex:Restaurant,Hospital,Resort,.....): ")
    area = input("Enter the Area(Ex: Durham, NC): ")
    num_pages = int(input("Enter the number of pages to scrape: "))

    scraped_data = scrape_yellowpages(keyword, area, num_pages)

    for i, item in enumerate(scraped_data):
        # Extract email information for each item
        website = item[1]
        email = extract_email_from_website(website)
        scraped_data[i] = item + (email,)

    output_filename = "output.csv"
    save_to_csv(scraped_data, output_filename)
    print(f"Scraped data saved to {output_filename}")
