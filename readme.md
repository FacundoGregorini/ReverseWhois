# Reverse WHOIS Wrapper
A tool to search for domains related with Name or Email via Reverse WHOIS pages.

---

## Installation
```bash
git clone https://github.com/FacundoGregorini/reverseWHOIS.git
cd reverseWHOIS/
python3 -m pip install -r requirements.txt
```
---
## Usage
```
usage: reverseWhois.py [-h]

optional arguments:
  -h, --help                                    Show this help message and exit
  -e EMAIL, --email EMAIL                       Input from email
  -n NAME [NAME ...], --name NAME [NAME ...]    Input from first and last name
  -f FORMAT, --format FORMAT {json, csv}        The format to use when exporting the data.
  -of OUTPUT_FILE, --output-file OUTPUT_FILE    The name of the file to save the data to.
```
---

## Examples

To search by Name
```
python3 reverseWhois.py -n John Doe Smith
```

To search by Email
```
python3 reverseWhois.py -e john.doe@gmail.com
```

To search by Email and save into a json file
```
python3 reverseWhois.py -e john.doe@gmail.com -f json -of example.json