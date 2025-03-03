import requests
from bs4 import BeautifulSoup
import json

# Headers to mimic real browser behavior
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
def extract_minutes(time_text):
    if not time_text:
        return 0  # Handle empty or None input

    words = time_text.split()
    
    if words[0].isdigit():  
        num = int(words[0])
        multiplier = 60 if "hour" in time_text else 1440 if "day" in time_text else 1
        return num * multiplier

    return 1 if "Just" in time_text else 0  # Handle "Just now", return 0 for unknown formats

def get_linkedin_job_ids(keyword, time_filter):
    """
    Fetches job IDs and times from LinkedIn with dynamic pagination.
    Stops when no jobs are found on a page.
    """
    formatted_keyword = keyword.replace(" ", "%2B")
    start_count = 0  # Dynamic pagination
    all_jobs = []  # Store all jobs across pages

    while True:
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={formatted_keyword}&location=United%2BStates&f_TPR=r86400&start={start_count}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        job_data = []
        for job in soup.find_all("li"):
            job_div = job.find("div", class_="base-card")
            job_id = job_div.get("data-entity-urn").split(":")[-1] if job_div and job_div.get("data-entity-urn") else None

            time_posted = job.find("time", class_="job-search-card__listdate--new")
            if job_id and time_posted:
                time_text = time_posted.text.strip()
                total_minutes = extract_minutes(time_text)

                job_data.append({"Job ID": job_id, "Time Posted": time_text, "Minutes": total_minutes})

        if not job_data:
            break  # Stop pagination when no jobs are found

        all_jobs.extend(job_data)
        start_count += 10  # Increment dynamically for pagination

    if not all_jobs:
        print("No jobs found.")
        return False

    return filter_job_ids(all_jobs, time_filter)


def filter_job_ids(job_data, time_filter):
    """
    Filters job IDs based on time criteria and saves filtered data.
    """
    filtered_ids = [job["Job ID"] for job in job_data if job["Minutes"] <= time_filter]

    if not filtered_ids:
        print("No jobs found within the specified time filter.")
        return False

    return scrape_job_details(filtered_ids)


def scrape_job_details(job_ids):
    """
    Scrapes job details for the given job IDs and saves to JSON.
    """
    job_list = []
    for job_id in job_ids:
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        job_response = requests.get(job_url, headers=HEADERS)

        if job_response.status_code == 200:
            job_soup = BeautifulSoup(job_response.text, "html.parser")

            title = job_soup.find("h2", class_=lambda x: x and "topcard__title" in x)
            company = job_soup.find("a", class_=lambda x: x and "topcard__org-name-link" in x)
            posted_time = job_soup.find("span", class_=lambda x: x and "posted-time-ago__text" in x)
            job_description = job_soup.find("div", class_=lambda x: x and "show-more-less-html__markup" in x)

            job_post = {
                "Job ID": job_id,
                "Apply Link": f"https://www.linkedin.com/jobs/view/{job_id}/",
                "Title": title.text.strip() if title else None,
                "Company Name": company.text.strip() if company else None,
                "Posted Time": posted_time.text.strip() if posted_time else None,
                "Job Description": job_description.get_text(separator=" ", strip=True) if job_description else None
            }

            job_list.append(job_post)

    return job_list


# Example Usage: Fetch jobs posted in the last 3 hours (180 minutes) and save to JSON
get_linkedin_job_ids("Data Engineer", time_filter=30)
