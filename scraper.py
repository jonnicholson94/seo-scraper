
from bs4 import BeautifulSoup
from lxml import etree
import requests

url = "https://lovespace.co.uk/sitemap.xml"
response = requests.get(url, timeout=5)
root = etree.fromstring(response.content)
xml = etree.tostring(root).decode()

url_list = xml.replace("<loc>", "").replace("</loc>", "").replace("</url>", "").replace("</urlset>", "").split("<url>")

results = []

for i in range(1, len(url_list)):
    result = { "url": url, "title": "", "description": "" }
    page = requests.get(url_list[1])
    soup = BeautifulSoup(page.content, "html.parser")
    if soup.findAll("meta", attrs={"name": "description"}):
        result["title"] = soup.find("meta", attrs={"name": "description"}).get("content")
    else:       
        result["title"] = 'No meta description found'
    if soup.findAll("meta", property="og:title"):
        result["description"] = soup.find("meta", property="og:title").get("content")
    else:
        result["description"] = "No meta description found"

    results.append(result)

