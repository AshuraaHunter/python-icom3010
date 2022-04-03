from queue import Empty
from bs4 import BeautifulSoup
import requests
import cfgScrape as cfg

class Listing:
    def __init__(self,title,company,location,date,link,keyworded):
        self.title = title
        self.company = company
        self.location = location
        self.date = date
        self.link = link
        self.keyworded = keyworded


"""
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
"""

def basic_scrape(title,city,prov,keywords):
    pNum = 1
    maxPNum = 1
    
    arr_listing = []
    
    if not city:
        prov += '-jobs'
        
    while pNum <= maxPNum:
        URL = f"https://www.careerbeacon.com/en/search/{title}-jobs-in-{city}_{prov}?page={pNum}"
        print(URL)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        
        pNumUL = soup.find('ul', class_="pagination")
        if pNumUL is None:
            print("ERROR: No results found.")
            return 0
        
        
        pNumLI = pNumUL.find_all('li')
        for li in pNumLI:
            try:
                maxPNum = min(cfg.settings["max_pages"],int(li.text.strip()))
            except ValueError:
                pass
        
        
            if li.has_attr('aria-label') and li['aria-label'] == "Last":
                break
    

        # removes the hidden 'in' that is for some reason on the CareerBeacon page
        for span in soup.find_all("span", class_="lower hidden-xs"): 
            span.decompose()

        results = soup.find(id="search_result")
        jobs = results.find_all("div", class_="non_featured_job_content")

        for job in jobs:
            job_title = job.find("div", class_="job_title")
            job_company = job.find("span", class_="name")
            job_location = job.find("span", class_="location") # this can be blank!
            job_date = (job.find("div", class_="job_pub_date")).attrs['title']
            job_link = (job.find("a")).attrs['href']
            
            arr_listing.append(Listing(job_title.text.strip(),job_company.text.strip(),job_location.text.strip(),job_date,job_link,False))

            
            print(job_title.text.strip()) # 'strip' allows us to cut out any interfering tags (but not their contents)
            print(job_company.text.strip())
            print(job_location.text.strip())
            print(job_date) # raw date is actually contained within the 'title' attribute, and here's how we extract it
            print(job_link)
            print('\n'*2)
            
        pNum += 1
    
    for listing in arr_listing:
        if keywords is None:
            break
        
        keyURL = listing.link
        keyPage = requests.get(keyURL)
        keySoup = BeautifulSoup(keyPage.content, "html.parser")
        keyInfoAlpha = keySoup.find("section", class_="details")
        
        if keyInfoAlpha is not None:
            keyInfo = keyInfoAlpha.text.strip()
        
        for keyword in keywords:
            if keyInfo is None or keyInfo is Empty:
                break
            elif keyInfo.find(keyword) != -1: # .find() returns -1 if its search is unsuccessful
                listing.keyworded = True
                break
            
    arr_listing.sort(key=lambda listing: listing.keyworded,reverse=True) # sorts the list in descending order based on if keywords were marked as present (True > False)
    
    return arr_listing

        
                
    
"""   
pNum = 1
maxPNum = 1
while pNum <= maxPNum:
    pNumUL = soup.find('ul', class_="pagination")
    pNumLI = pNumUL.find_all('li')
    for li in pNumLI:
        try:
            maxPNum = int(li.text.strip())
        except ValueError:
            pass
        
        
        if li.has_attr('aria-label') and li['aria-label'] == "Last":
            break
    
    pNum += 1
    
    URL = f"https://www.careerbeacon.com/en/search/{searchFor}-jobs-in-{searchCity}_{searchProv}?page={pNum}"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    # removes the hidden 'in' that is for some reason on the CareerBeacon page
    for span in soup.find_all("span", class_="lower hidden-xs"): 
        span.decompose()

    results = soup.find(id="search_result")
    jobs = results.find_all("div", class_="non_featured_job_content")

    for job in jobs:
        job_title = job.find("div", class_="job_title")
        job_company = job.find("span", class_="name")
        job_location = job.find("span", class_="location") # this can be blank!
        job_date_input = job.find("div", class_="job_pub_date")
        job_date = job_date_input.attrs['title']
    
        print(job_title.text.strip()) # 'strip' allows us to cut out any interfering tags (but not their contents)
        print(job_company.text.strip())
        print(job_location.text.strip())
        print(job_date) # raw date is actually contained within the 'title' attribute, and here's how we extract it
        print('\n'*2)

    # we can also do this but it returns irrelevant results? so probably avoid it
    if pNum == maxPNum:
        featured_jobs = results.find_all("div", class_="featured_job_content")

        for featured_job in featured_jobs:
            featured_title = featured_job.find("div", class_="job_title")
            featured_company = featured_job.find("span", class_="name")
            featured_location = featured_job.find("div", class_="job_location mid-grey")
            featured_date_input = featured_job.find("div", class_="job_pub_date")
            featured_date = featured_date_input.attrs['title']
    
            print(featured_title.text.strip())
            print(featured_company.text.strip())
            print(featured_location.text.strip())
            print(featured_date)
            print('\n'*2)
"""
    
    
    
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
