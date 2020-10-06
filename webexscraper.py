import re
import requests
import urllib.request
import time
from bs4 import BeautifulSoup


# From WebExDomain Table get only domain names with wildcards
def grab_domains(data):
    domainList = []
    for lines in data:
        domains = lines[1].split(' ')
        cleanDomain = " ".join(re.findall("([\^]*[\*\.]*[a-z0-9]+\.+.*)*", domains[0]))

        # Strip Whitespace lines to remove blank values
        cleanDomain = cleanDomain.strip()

        # Dedup List
        if cleanDomain not in domainList:
            if len(cleanDomain) > 0:
                domainList.append(cleanDomain)
    return domainList

def grab_ips(data):
    ipList = []
    for lines in data:
        for line in lines:
            values = line.split(' (CIDR)')
            cleanCidr = " ".join(re.findall("([0-9]+\.+[0-9]+\.+[0-9]+\.+[0-9]+\/[0-9]+)", values[0]))

            # Strip Whitespace lines to remove blank values
            cleanCidr = cleanCidr.strip()
            # Dedup List
            if cleanCidr not in ipList:
                if len(cleanCidr) > 0:
                    ipList.append(cleanCidr)
    return ipList

def grab_domain_table(html_section):
    # Get Clean List of Domains
    table = html_section.find('table', attrs={'class': 'li'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    return data


def grab_ip_table(html_section):
    rows = html_section.find_all('ul')
    data = []
    for row in rows:
        cols = row.find_all('li')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    return data


url = "https://help.webex.com/en-us/WBX264/How-Do-I-Allow-Webex-Meetings-Traffic-on-My-Network#id_135010"
response = requests.get(url)

print("Response:" + str(response))

soup = BeautifulSoup(response.text, "html.parser")

# Get the IP and Domain Sections from WebEx website
ipsSection = soup.find("div", {"id": "id_135011"})
domainsSection = soup.find("div", {"id": "id_135010"})

# Get Domains from domain table
domainTable = grab_domain_table(domainsSection)
retDomains = grab_domains(domainTable)

# Get IPS from IP Table
ipTable = grab_ip_table(ipsSection)
retIPs = grab_ips(ipTable)

print(retIPs)
print(retDomains)