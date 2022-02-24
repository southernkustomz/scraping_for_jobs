import requests
import bs4
import pandas as pd
import time


print("-----------------Web scraping jobs on Indeed.com--------------------")

# Ask the user for all of the search parameters
job_search = input("What keywords would you like to use? ").replace(" ", "%20")

city_set = [str(input("What city should I look in? ").replace(" ", "%20"))]

print("There are 15 results per page.")
max_pages_per_city = int(input("How many pages should I check? ")) * 10

# Create a data frame to hold the job posting information.
sample_df = pd.DataFrame(columns=["city", "job_title", "company", "location", "link"])

# Scraping code
for city in city_set:
    for start in range(0, max_pages_per_city, 10):
        page = requests.get(
            'https://www.indeed.com/jobs?q=' + str(job_search) + '&l=' + str(city) + '%2C%20TX&radius=50&start=' + str(
                start))
    # wait 1 second between page grabs
        time.sleep(1)
        soup = bs4.BeautifulSoup(page.text, "lxml")

        for table in soup.find_all("td", class_="resultContent"):
# specifying row number for index of job postings
            num = len(sample_df) + 1

# creating empty list to hold posting data
            job_post = []
# grabbing the job title
            div = table.find("h2", class_="jobTitle")
            comp = table.find("span", class_="companyName")
            loc = table.find("div", class_="companyLocation")
            link = table.find_parent("a")

# Append each item to the job post list
            job_post.append(city)
            job_post.append(div.text)
            job_post.append(comp.text)
            job_post.append(loc.text)
            job_post.append("www.indeed.com" + link.get("href"))

# append the job post list to the dataframe at index num
            sample_df.loc[num] = job_post

# save sample_df as a local csv file
sample_df.to_csv("jobs.csv")
print("Search Complete. Your file is ready to view.")
