import argparse
import requests
from bs4 import BeautifulSoup
import json
import random
import pandas as pd
from prettytable import PrettyTable
import csv

def exportToCSV(data, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def exportToJson(data, filename):
    with open(filename, "w") as file:
        file.write(json.dumps(data, indent=4))

def getRandomUserAgent():
    rdm = random.randint(0, 9)
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",    
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/85.0.4183.121 Safari/537.36",    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/91.0.864.63",    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Brave/2.11.97",    
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15 Brave/1.20.103",    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edge/91.0.864.63",    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 SamsungBrowser/13.2",    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 EdgA/91.0.864.63"]
    return user_agents[rdm]

def getWhoxyByName(name):
    text = ""
    name = name.lower().split(" ")
    for range in name:
        text += range + "+"
    user_agent = {"User-Agent": "{}".format(getRandomUserAgent())}
    url = "https://www.whoxy.com/search.php?name={}".format(text[:-1], headers=user_agent)
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", class_="grid first_col_center")

        headers = [header.text for header in table.find_all("th")]
        rows = []
        for row in table.find_all("tr")[1:]:
            cells = [cell.text for cell in row.find_all("td")]
            rows.append(cells)

        df = pd.DataFrame(rows, columns=headers)

        return df.to_json(orient="records")

def getWhoxyByEmail(mail):
    user_agent = {"User-Agent": "{}".format(getRandomUserAgent())}
    url = "https://osint.sh/reversewhois/".format(mail)
    r = requests.post(url, headers=user_agent, data={"email": mail})
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find( "table", {"class":"bmw-table css-serial"} )

        headers = [header.text for header in table.find_all("th")]
        rows = []
        for row in table.find_all("tr")[1:]:
            cells = [cell.text.strip() for cell in row.find_all("td")]
            rows.append(cells)
        
        df = pd.DataFrame(rows, columns=headers)

        return df.to_json(orient="records")


##Main
parser = argparse.ArgumentParser(description='Reverse Whois')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e', '--email', type=str, help='Input from email')
group.add_argument('-n', '--name', type=str, nargs='+', help='Input from first and last name')
parser.add_argument('-f', '--format', type=str, help='The format to use when exporting the data (json, csv).', required=False)
parser.add_argument('-of', '--output-file', type=str, help='The name of the file to save the data to.', required=False)

args = parser.parse_args()

if args.email:
    resEmail = getWhoxyByEmail(args.email)
    data = json.loads(resEmail)
    if args.format == 'json':
        exportToJson(data, args.file)
    elif args.format == 'csv':
        exportToCSV(data, args.file)
    else:
        table = PrettyTable(['Domain', 'Registrar', 'Created', 'Expired', 'Owner', 'Phone', 'Address'])
        for row in data:
            table.add_row([row["Domain"], row["Registrar"], row["Created"], row["Expired"], row["Owner"], row["Phone"], row["Address"].strip()])
        print(table)
elif args.name:
    full_name = " ".join(args.name)
    resName = getWhoxyByName(full_name)
    data = json.loads(resName)
    if args.format == 'json':
        exportToJson(data, args.file)    
    elif args.format == 'csv':
        exportToCSV(data, args.file)
    else:
        table = PrettyTable(['Domain Name','Registrar','Created','Updated','Expiry'])
        for row in data:
            table.add_row(row['Domain Name'],row['Registrar'],row['Created'],row['Updated'],row['Expiry'])
        print(table)