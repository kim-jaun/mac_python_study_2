import requests
from bs4 import BeautifulSoup


def get_last_pages(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company != None:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = company_anchor.string
        else:
            company = company.string
        company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    if "NoneType" in html["data-jk"]:
        None
    else:
        job_id = html["data-jk"]

    return {
        'title': title,
        'company': company,
        'location': location,
        "link": f"https://kr.indeed.com/jobs?q=python&vjk={job_id}"
    }


def extract_jobs(last_pages, url, limit):
    jobs = []
    for page in range(last_pages):
      print(f"Scrapping indeed: Page {page}")
      result = requests.get(f"{url}&start={page*limit}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
      for result in results:
          job = extract_job(result)
          jobs.append(job)
    return jobs

def get_jobs(word):
  limit = 50
  url = f"https://kr.indeed.com/취업?q={word}&limit={limit}"
  last_page = get_last_pages(url)
  jobs = extract_jobs(last_page, url, limit)
  return jobs

