import requests
from bs4 import BeautifulSoup

searchFor = input("Enter a job title: ")
searchFor = searchFor.replace(' ','-')
print(searchFor)

searchCity = input("Enter a town / city: ")
searchCity = searchCity.replace(' ','-')
print(searchCity)

searchProv = input("Enter a province: ")
searchProv = searchProv.replace(' ','-')
print(searchProv)

searchKey = input("Enter a keyword you'd like to filter by: ")
print(searchKey)

URL = f"https://www.careerbeacon.com/en/search/{searchFor}-jobs-in-{searchCity}_{searchProv}"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# removes the hidden 'in' that is for some reason on the CareerBeacon page
for span in soup.find_all("span", {'class':'lower hidden-xs'}): 
    span.decompose()

results = soup.find(id="search_result")
jobs = results.find_all("div", class_="non_featured_job_content")

for job in jobs:
    job_title = job.find("div", class_="job_title")
    job_company = job.find("span", class_="name")
    job_location = job.find("span", class_="location")
    
    print(job_title.text.strip()) # 'strip' allows us to cut out any interfering tags (but not their contents)
    print(job_company.text.strip())
    print(job_location.text.strip())
    print('\n'*2)

# we can also do this but it returns irrelevant results? so probably avoid it
featured_jobs = results.find_all("div", class_="featured_job_content")

for featured_job in featured_jobs:
    featured_title = featured_job.find("div", class_="job_title")
    featured_company = featured_job.find("span", class_="name")
    featured_location = featured_job.find("div", class_="job_location mid-grey")
    
    print(featured_title.text.strip())
    print(featured_company.text.strip())
    print(featured_location.text.strip())
    print('\n'*2)
    
"""
key_jobs = results.find_all(
    "div", string=lambda text: f"{searchKey}" in text.lower()
)
key_job_elements = [
    div_element.parent.parent.parent for div_element in key_jobs
]
for job_element in key_job_elements:
    # -- snip --
    link_url = job_element.find_all("a")["href"]
    print(f"Apply here: {link_url}\n")
        
print(len(key_jobs))
"""
