
from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd

url = "https://lovespace.co.uk/sitemap.xml"
response = requests.get(url, timeout=5)
root = etree.fromstring(response.content)
xml = etree.tostring(root).decode()

url_list = xml.replace("<loc>", "").replace("</loc>", "").replace("</url>", "").replace("</urlset>", "").split("<url>")

titles = []
descriptions = []

url_list.pop(0)

for i in range(0, len(url_list)):
    page = requests.get(url_list[i])
    soup = BeautifulSoup(page.content, "html.parser")
    if soup.findAll("meta", attrs={"name": "description"}):
        titles.append(soup.find("meta", attrs={"name": "description"}).get("content"))
    else:       
        titles.append('No meta description found')
    if soup.findAll("meta", property="og:title"):
        descriptions.append(soup.find("meta", property="og:title").get("content"))
    else:
        descriptions.append("No meta description found")


data = {
    'page_url': url_list,
    'titles': titles,
    'descriptions': descriptions
}

df = pd.DataFrame(data)

df.to_excel("~/Downloads/results.xlsx", index=False)