import requests
import time
import os
 
# Clearing the Screen

def check_page_status(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
while True:
    url = "https://cetonline.karnataka.gov.in/keavsslip2024/forms/vrslip2024.aspx"
    print('-------------------------')
    print(check_page_status(url))
    print('-------------------------')
    time.sleep(4)
    os.system('cls')